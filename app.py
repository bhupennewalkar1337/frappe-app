from flask import Flask, render_template, redirect, request, url_for, make_response, flash
from flask.ext.script import Manager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate, MigrateCommand
import os

from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Required, NumberRange

from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)

# Edit this line. Line should be specified as
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@hostname/database' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/shop'

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SECRET_KEY'] = 'hard to guess string'

db = SQLAlchemy(app)
manager = Manager(app)
Bootstrap(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/goodsreceipt/')
def goods_receipt():
    goods = Goods.query.all()
    return render_template("goodsreceipt.html", goods=goods)
    
@app.route('/stockin', methods=['GET', 'POST'])
def stock_in():
    form = StockInForm()
    if form.validate_on_submit():
        stock_no = form.stock_no.data
        doc_qnt = form.doc_qnt.data
        item_desc = form.item_desc.data
        selling_price = form.selling_price.data
        current_cost = form.current_cost.data
        
        if Goods.query.filter_by(stock_no=stock_no).first():
            return "Stock Number already present"
        
        good = Goods(stock_no=stock_no, act_qnt=doc_qnt, item_desc=item_desc, selling_price=selling_price, current_cost=current_cost)
        db.session.add(good)
        db.session.commit()
        return redirect('goodsreceipt')
    return render_template('stockin.html', form=form)
    
@app.route('/stockout', methods=['GET', 'POST'])
def stock_out():
    form = StockOutForm()
    if form.validate_on_submit():
        stock_no = form.stock_no.data
        quantity = form.quantity.data
        
        good = Goods.query.filter_by(stock_no=stock_no).first()
        
        if not good:
            return "Stock Number Invalid"
        elif good.act_qnt >= int(quantity):
            good.act_qnt -= int(quantity)
            db.session.add(good)
            db.session.commit()
            
            if(good.act_qnt < 10):
                flash("Quantity of stock " + str(good.stock_no) + " is getting low. Order it soon.")
            return redirect('goodsreceipt')
        else:
            return "Not enough items present"
    return render_template('stockout.html', form=form)
    
class Goods(db.Model):
    __tablename__ = 'goods'
    stock_no = db.Column(db.Integer, primary_key=True)
    act_qnt = db.Column(db.Integer)
    item_desc = db.Column(db.String(64))
    selling_price = db.Column(db.Float)
    current_cost = db.Column(db.Float)
    
    def __repr__(self):
        return '<Good %r %r %r>' % (self.stock_no, self.act_qnt, self.item_desc)

class StockInForm(Form):
    stock_no = StringField("Stock Number")
    doc_qnt = StringField("Docet Quantity")
    item_desc = SelectField("Item Description", choices=[('shirt', 'Shirt'), ('trouser', 'Trouser'), ('blazer', 'Blazer'), ('tshirt', 'T Shirt')])
    selling_price = StringField("Selling price")
    current_cost = StringField("Current Cost")
    submit = SubmitField("Add")

class StockOutForm(Form):
    stock_no = StringField("Stock Number")
    quantity = StringField("Quantity")
    submit = SubmitField("Sell")
    
manager.run()

