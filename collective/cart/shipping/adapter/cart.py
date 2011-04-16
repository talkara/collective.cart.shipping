from Acquisition import aq_inner
from zope.interface import implements
from zope.component import adapts, getUtility, getMultiAdapter
from Products.ZCatalog.interfaces import IZCatalog
from Products.CMFCore.utils import getToolByName
from collective.cart.core.adapter.cart import CartItself
from collective.cart.core.content import CartProduct
from collective.cart.core.interfaces import (
    ICart,
    ICartItself,
    ICartAdapter,
    ICartProduct,
    ICartProductAdapter,
    ICartProductOriginal,
    IProduct,
    IProductAnnotationsAdapter,
    ISelectRange,
    IShippingCost,
)
from collective.cart.shipping.interfaces import (
    IShippingMethodAdapter,
)


#class ShippingCost(object):

#    adapts(ICart)
#    implements(IShippingCost)

#    def __init__(self, context):
#        self.context = context

#    def __call__(self):
#        method = self.context.shipping_method
#        IShippingMethodAdapter(method)

class CartItself(CartItself):

    @property
    def products(self):
        return self.context.objectValues()

    @property
    def weight(self):
        method = self.context.shipping_method
        weights = [
            ICartProductAdapter(product).weight_in_kg(method) for product in self.products
        ]
        return sum(weights)

    @property
    def shipping_cost(self):
        sma = IShippingMethodAdapter(self.context.shipping_method)
        return sma.shipping_cost(self.weight, self.subtotal)