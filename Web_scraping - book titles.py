import scrapy
from scrapy import Request
                                              
class GetbooksSpider(scrapy.Spider):
    name = "getbooks"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]
    
    def parse(self,response):
        books = response.xpath('//article[@class="product_pod"]')
  
        for book in books:
            price = book.xpath('div/p[@class="price_color"]/text()').extract_first()[1:-1]
            star  = book.xpath('p/@class').extract_first()[11:]
            #star = [rating.replace("star-rating ","") for rating in star] 
            
            rel_url=book.xpath('h3/a/@href').extract_first()
            abs_url= response.urljoin(rel_url)
            
            yield Request(abs_url,callback = self.parse_page,
                  meta = {"Price":price,"Rating":star,"URL":abs_url})
                
        rel_next_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
        abs_next_url = response.urljoin(rel_next_url)
        
        yield Request(abs_next_url,callback=self.parse)
        
    def parse_page(self,response):
        price=response.meta.get('Price')
        star= response.meta.get('Rating')
        url = response.meta.get('URL')
        title = response.xpath('//div/h1/text()').extract_first()
        availability = response.xpath('//div/p[@class="instock availability"]/text()').extract()[1].strip()
        #description = response.xpath('//article[@class="product_description"]/p/text()').extract_first().strip()
        description = response.xpath('//article[@class="product_page"]/p/text()').extract_first().strip()
        yield{"Title":title,"Price":price,"Rating":star,"URL":url,"Availability":availability,"Description":description}
        
     

    