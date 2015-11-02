from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns("goods.views",
                       url(r"^add_goods/$", "show_add_goods"),
                       url(r"^add_type/$", "show_add_type"),
                       url(r"^goods_manage/$", "show_manage"),
                       url(r"^do_add_goods/$", "add_goods"),
                       url(r"^do_add_type/$", "add_type"),
                       url(r"^do_type_props/$", "do_type_props"),
                       url(r"^do_accept_purchase/$", "do_accept_purchase"),
                       url(r"^do_reject_purchase/$", "do_reject_purchase"),
                       url(r"^do_finish_purchase/$", "do_finish_purchase"),
                       url(r"^do_accept_borrow/$", "do_accept_borrow"),
                       url(r"^do_reject_borrow/$", "do_reject_borrow"),
                       url(r"^do_finish_borrow$", "do_finish_borrow"),
                       url(r"^do_accept_return/$", "do_accept_return"),
                       url(r"^do_finish_return/$", "do_finish_return"),
                       url(r'^do_borrow/$', "do_borrow"),
                       url(r'^borrow/$', "show_borrow"),
                       url(r"^list/$", "show_list"),
                       url(r"^do_set_available/$", "do_set_available"),
                       url(r"^do_set_unavailable/$", "do_set_unavailable"),
                       url(r"^do_destroy/$", "do_destroy"),
                       url(r"^do_return_goods", "do_return_goods"),
                       url(r"^do_miss_goods", "do_miss_goods"),
                       url(r"^do_accept_repair", "do_accept_repair"),
                       url(r"^do_do_start_repair", "do_start_repair"),
                       url(r"^do_do_finish_repair", "do_finish_repair"),
                       url(r"^do_return_repair", "do_return_repair"),
                       url(r"^do_repair_goods", "do_repair_goods"),
                       url(r"^do_reject_repair", "do_reject_repair"),
                       url(r"^show_borrow_list", "show_borrow_list"),
                       url(r'^show_request_purchase$', "show_request_purchase"),

                       url(r'^do_purchase$', "do_purchase"),

                       url(r'^show_request_exist_purchase', "show_request_exist_purchase")

                       )
