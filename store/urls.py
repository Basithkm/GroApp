
from . import views
from rest_framework import routers


router=routers.DefaultRouter()

router.register('products',views.ProductViewSet,basename="product")
router.register('category',views.CategoryViewSet),
router.register('review',views.ReviewViewSet),
router.register('banner',views.BannerViewSet),
router.register('carts',views.CartViewSet,basename="carts")
urlpatterns = router.urls
