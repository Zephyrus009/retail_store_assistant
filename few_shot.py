examples = [
    {
        'Question':"How much discount we provided in between april to december to ladies customers on Beauty products ?",
        'SQLQuery':"select sum(discount_pct) as Discounts from (select product_code.discount_pct, retail_data.customer_id, retail_data.gender, retail_data.product_category, retail_data.date from retail_data inner join product_code on product_code.product_category = retail_data.product_category) s1 where date between '01-04-2023' and '31-12-2023' and gender = 'Female' and product_category = 'Beauty'",
        'SQLResult': "[(3280,)]",
        "Answer": "3280"

    }
]