"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from VintGizmo import views
from VintGizmo.views import auth_views
from VintGizmo.views import home_views
from VintGizmo.views import product_views
from VintGizmo.views import Dashboard_views
from VintGizmo.views import category_views
from VintGizmo.views import brand_views
from VintGizmo.views import Image_views
from VintGizmo.views import product_detail_views
from VintGizmo.views import ProductVariationDetail_views
from VintGizmo.views import cart_views
from VintGizmo.views import address_views
from VintGizmo.views import checkout_views
from VintGizmo.views import order_views
from VintGizmo.views import reviews_views
from VintGizmo.views import banner_views
from VintGizmo.views import store_reviews_views
from VintGizmo.views import coupon_views
from VintGizmo.views import search_filter_views
urlpatterns =[
    path('admin/', admin.site.urls),
    
# Auth urls
path('loginPage/',auth_views.Login_Page,name='loginPage'),
path('registerPage/',auth_views.register_Page,name='registerPage'),
path('VerifyPage/',auth_views.VerifyPage,name='VerifyPage'),
path('logout/', auth_views.user_logout, name='logout'),
path('Authregister/',auth_views.RegisterAPI.as_view(),name='register'),
path('Verify/',auth_views.VerifyOTP.as_view(),name='Verify'),
path('AuthLogin/',auth_views.LoginAPI.as_view(),name='AuthLogin'),
path('super/',auth_views.admin_Page,name='super'),
path('staff/',auth_views.staff_Page,name='staff'),
path('resend-otp/',auth_views.resend_otp, name='resend_otp'),
path('Forgot',auth_views.ForgotPassword, name='ForgotPassword'),
path('ForgotPage',auth_views.ForgotPasswordPage, name='ForgotPasswordPage'),
path('New',auth_views.NewPasswordPage, name='NewPasswordPage'),
path('Change',auth_views.ChangePassword, name='Change'),
path('VerifyEmail',auth_views.VerifyEmailPage, name='EmailVerify'),


# Admin urls
path('AdminP/',Dashboard_views.admin_dashboard,name='AdminPanel'),
 # URL for monthly sales and profits data
    path('api/monthly-sales-profits/', Dashboard_views.monthly_sales_profits, name='monthly_sales_profits'),

    # URL for annual sales and profits data
    path('api/annual-sales-profits/', Dashboard_views.annual_sales_profits, name='annual_sales_profits'),

# Product urls
 path('product',product_views.Product_Page,name='product_management'),
 path('AddProduct',product_views.SaveProduct,name='AddProduct'),
 path('UpdateProducts',product_views.update_product,name='UpdateProduct'),
 path('DeleteProduct/<int:id>',product_views.delete_product,name='DeleteProduct'),
path('product/get/<int:id>/', product_views.get_product_data, name='get_product_data'),
# Sold Products
path('sold-products',product_views.sold_products,name="sold_products"),

# brand urls
path('Addbrand',brand_views.SaveBrand,name='AddBrand'),
path('getBrands/',brand_views.get_brands, name='get_brands'),
path('delete-brand/<int:id>',brand_views.delete_brand,name="deleteBrand"),

# category urls
path('AddCategory',category_views.SaveCategory,name='SaveCategory'),
path('getCategories/', category_views.get_categories, name='get_categories'),
path('delete-category/<int:id>',category_views.delete_catogery,name="deleteCategory"),
# Image url
path('AddImage',Image_views.add_image,name='AddImage'),
path('DeleteImage/<int:id>',Image_views.DeleteImage, name='DeleteImage'),
# Variations url
path('Detail_Page/<int:id>/', product_detail_views.detail_page, name="DetailPage"),
 path('UpdateVariation',product_detail_views.update_variation,name='UpdateVariation'),
path('AddVariation',product_detail_views.add_variation,name="AddVariation"),
path('variation/get/<int:id>/', product_detail_views.get_variation_data, name='get_variation_data'),
path('deletevarition/<int:id>/',product_detail_views.delete_variation,name='Delete'),
path('get/variation/<int:id>/',product_detail_views.get_variation_data,name='getVariationData'),
path('ProductVarationDetail/<int:id>/',ProductVariationDetail_views.Product_V_D_Page,name="V_D"),
# Home Page views
path('',home_views.HomePage,name='Home'),
path('ProductPage',home_views.ProductPage,name='ProductPage'),
path('Details/<int:id>/',home_views.ProductDetail,name='Detail'),
path('variation/<int:id>/', home_views.get_variation_details, name='get_variation_details'),
    path('dynamic-styles.css', home_views.dynamic_css, name='dynamic_css'),
    path('search/', search_filter_views.search_home_page, name='search_home_page'),

# Cart  Views
path('Cart',cart_views.CartPage,name="CartPage"),
path('add-to-cart/<int:product_id>/<int:variation_id>/', cart_views.add_to_cart, name='add_to_cart'),
path('update-cart-item/<int:cart_item_id>/', cart_views.update_cart_item, name='update_cart_item'),
path('delete-cart-item/<int:id>/', cart_views.delete_cart_item, name='delete_cart_item'),
# Adress Views
path('Address',address_views.user_addresses,name="AddressPage"),
path('AddAddress',address_views.add_address,name="AddAddress"),
path('addresses/<int:id>/', address_views.address_detail, name='address_detail'),
path('addresses/update/', address_views.update_address, name='update_address'),
path('DeleteAddress/<int:id>/', address_views.delete_address, name='DeleteAddress'),

# CheckOut Views
path('CheckoutPage/',checkout_views.CheckOutPage,name="CheckOutPage"),
path('set-selected-items/', checkout_views.store_selected_items, name='store_selected_items'),
# order Views
path('checkout/order/', order_views.create_order, name='create_order'),
path('DeleteOrder/<int:id>/',order_views.delete_order,name="DeleteOrder"),
path('UpdateStatus',order_views.change_status,name="ChangeStatus"),
 path('get-order-id/', order_views.get_order_id, name='get_order_id'),
path('CompletedOrders',order_views.completed_orders_page,name="CompletedOrderPage"),
path('PendingOrders',order_views.pending_orders_page,name="PendingOrderPage"),
path('ShippedOrders',order_views.shipped_orders_page,name="ShippedOrderPage"),
path('CancelledOrders',order_views.cancelled_orders_page,name="CancelledOrderPage"),
path('Order_Items/<int:id>/',order_views.order_items,name="Order_Item"),
# Review Views
    path('submit-review/', reviews_views.submit_review, name='submit_review'),
    path('show-all-reviews/<int:id>/', reviews_views.show_all_reviews, name='show_all_reviews'),
     path('fetch-reviews/<int:id>/', reviews_views.fetch_reviews, name='fetch_reviews'),
     path('fetch-all-reviews/<int:id>/', reviews_views.fetch_all_reviews, name='fetch_all_reviews'),
     path('variation-review/<int:id>/',reviews_views.review_page,name="ReviewPage"),

# Track Order Views
path('track-order-page',order_views.track_order_page,name="TrackOrder"),
    path('track-order/', order_views.track_order, name='track_order'),

# Banner Views
path('destroy-home-banner/', banner_views.destroy_home_banner, name='destroy_home_banner'),
    path('save-home-banner/', banner_views.save_home_banner, name='save_home_banner'),
    path('save-sale-banner/', banner_views.save_sale_banner, name='save_sale_banner'),
    path('delete-sale-banner/', banner_views.delete_sale_banner, name='delete_sale_banner'),
    path('save-home-image/', banner_views.save_home_image, name='save_home_image'),
    path('update-home-image/', banner_views.update_home_image, name='update_home_image'),
    path('delete-home-image/<int:image_id>/', banner_views.delete_home_image, name='delete_home_image'),
    path('home-banner/', banner_views.HomeBannerPage, name='home_banner'),
    path('sale-banner/', banner_views.SaleBannerPage, name='sale_banner'),
    path('home-images/', banner_views.HomeImagesPage, name='home_images'),

#store reviews
    path('reviews/create/', store_reviews_views.create_review, name='create_review'),
    path('reviews/update/', store_reviews_views.update_review, name='update_review'),
    path('reviews/<int:review_id>/delete/', store_reviews_views.delete_review, name='delete_review'),
    path('pending/reviews',store_reviews_views.pending_reviews,name='pending_store_reviews'),
    path('approved/reviews',store_reviews_views.approved_reviews,name='approved_store_reviews'),
    path('rejected/reviews',store_reviews_views.rejected_reviews,name='rejected_store_reviews'),
    path('create-review-ajax/', store_reviews_views.create_review_ajax, name='create_review_ajax'),


# Coupon 
path('coupons',coupon_views.coupon_page,name="coupon_page"),
path('save-coupon',coupon_views.save_coupon,name="save_coupon"),
path('update-coupon',coupon_views.update_coupon,name="update_coupon"),
path('delete-coupon/<int:coupon_id>/',coupon_views.delete_coupon,name="delete_coupon"),
    path('apply-coupon/', coupon_views.apply_coupon, name='apply_coupon'),  # Add this line

# payment
path('success',order_views.success_page,name="success_page"),
path('payment/<int:payment>/', order_views.Payment, name='payment'),

#extra  pages
path('refund',home_views.refund_page,name="Refund"),
path('terms-of-use',home_views.terms_of_use_page,name="Terms"),
path('privacy-policy',home_views.privacy_policy_page,name="Privacy"),
path('contact-us',home_views.contact_us_page,name="contact"),
path('my-profile',home_views.user_profile_page,name="profile"),
path('user-orders/', home_views.user_orders_view, name='user_orders'),


#for contact us form
    path('contact/', home_views.contact_form, name='contact_form'),

#functoin for updating the customer's phone profile image and username
    path('update-profile/', home_views.profile_save, name='update_profile'),
#


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
