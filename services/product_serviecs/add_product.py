
def add_Product(db,Product, User, product_name, price, description, stock, username, image_url):

       user = User.query.filter_by(username=username).first()

       try:
           new_Product = Product(
               product_name=product_name,
               price=price,
               image_url=image_url,
               description=description,
               stock=stock,          
               user_id=user._id
           )
           db.session.add(new_Product)
           db.session.commit()
           return("your last product has been added successfully!")
       except ValueError as e:
           db.session.rollback()
           return (str(e))


