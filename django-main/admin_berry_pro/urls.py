from django.urls import path
from admin_berry_pro import views

from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index),
    
    # Dashboard
    path('dashboard/', views.default, name='dashboard_index'),
    path('dashboard/analytics/', views.analytics, name='analytics'),

    # Widgets
    path('widgets/statistics/', views.statistics, name='statistics'),
    path('widgets/data/', views.data, name='data'),
    path('widgets/chart/', views.chart, name='chart'),

    # Layout
    path('layout/vertical/', views.vertical_layout, name='vertical_layout'),
    path('layout/horizontal/', views.horizontal_layout, name='horizontal_layout'),
    path('layout/compact/', views.compact_layout, name='compact_layout'),

    # Application
    path('application/social-profile/', views.social_profile, name='social_profile'),
    path('application/account-profile/v1/', views.account_profile_v1, name='account_profile_v1'),
    path('application/account-profile/v2/', views.account_profile_v2, name='account_profile_v2'),
    path('application/account-profile/v3/', views.account_profile_v3, name='account_profile_v3'),
    path('application/user-card/v1/', views.user_card_v1, name='user_card_v1'),
    path('application/user-card/v2/', views.user_card_v2, name='user_card_v2'),
    path('application/user-card/v3/', views.user_card_v3, name='user_card_v3'),
    path('application/user-list/v1/', views.user_list_v1, name='user_list_v1'),
    path('application/user-list/v2/', views.user_list_v2, name='user_list_v2'),
    path('application/customer-list/', views.customer_list, name='customer_list'),
    path('application/order-list/', views.order_list, name='order_list'),
    path('application/order-details/', views.order_details, name='order_details'),
    path('application/create-invoice/', views.create_invoice, name='create_invoice'),
    path('application/product-list/', views.product_list, name='product_list'),
    path('application/product-review/', views.product_review, name='product_review'),
    path('application/chat/', views.chat, name='chat'),
    path('application/kanban/', views.kanban, name='kanban'),
    path('application/mail/', views.mail, name='mail'),
    path('application/calendar/', views.calendar, name='calendar'),
    path('application/contact-cards/', views.contact_cards, name='contact_cards'),
    path('application/contact-list/', views.contact_list, name='contact_list'),
    path('application/ecommerce-product/', views.ecom_product, name='ecom_product'),
    path('application/ecommerce-product-details/', views.ecom_product_details, name='ecom_product_details'),
    path('application/ecommerce-product-list/', views.ecom_product_list, name='ecom_product_list'),
    path('application/ecommerce-checkout/', views.ecom_checkout, name='ecom_checkout'),

    # Basic Elements
    path('elements/alerts/', views.alerts, name='alerts'),
    path('elements/button/', views.button, name='button'),
    path('elements/badges/', views.badges, name='badges'),
    path('elements/breadcrumb-pagination/', views.breadcrumb_pagination, name='breadcrumb_pagination'),
    path('elements/card/', views.card, name='card'),
    path('elements/carousel/', views.carousel, name='carousel'),
    path('elements/collapse/', views.collapse, name='collapse'),
    path('elements/color/', views.color, name='color'),
    path('elements/dropdowns/', views.dropdowns, name='dropdowns'),
    path('elements/extra/', views.extra, name='extra'),
    path('elements/grid/', views.grid, name='grid'),
    path('elements/list-group/', views.list_group, name='list_group'),
    path('elements/modal/', views.modal, name='modal'),
    path('elements/offcanvas/', views.offcanvas, name='offcanvas'),
    path('elements/progress/', views.progress, name='progress'),
    path('elements/spinner/', views.spinner, name='spinner'),
    path('elements/tabs/', views.tabs, name='tabs'),
    path('elements/toasts/', views.toasts, name='toasts'),
    path('elements/tooltip-popover/', views.tooltip_popover, name='tooltip_popover'),
    path('elements/typography/', views.typography, name='typography'),

    # Advance Elements
    path('elements/sweet-alerts/', views.sweet_alert, name='sweet_alert'),
    path('elements/datepicker/', views.datepicker, name='datepicker'),
    path('elements/lightbox/', views.lightbox, name='lightbox'),
    path('elements/ac-modal/', views.ac_modal, name='ac_modal'),
    path('elements/notification/', views.notification, name='notification'),
    path('elements/range-slider/', views.range_slider, name='range_slider'),
    path('elements/slider/', views.slider, name='slider'),
    path('elements/syntax-highlighter/', views.syntax_highlighter, name='syntax_highlighter'),
    path('elements/tour/', views.tour, name='tour'),
    path('elements/tree-view/', views.tree_view, name='tree_view'),

    # Icons
    path('elements/feather/', views.feather, name='feather'),
    path('elements/fontawesome/', views.font_awesome, name='font_awesome'),
    path('elements/material/', views.material, name='material'),
    path('elements/tabler/', views.tabler, name='tabler'),

    # Forms
    path('forms/form-basic/', views.form_elements, name='form_elements'),
    path('forms/form-floating/', views.form_floating, name='form_floating'),
    path('forms/form-options/', views.form_options, name='form_options'),
    path('forms/input-group/', views.input_groups, name='input_groups'),
    path('forms/checkbox/', views.checkbox, name='checkbox'),
    path('forms/radio/', views.radio, name='radio'),
    path('forms/switch/', views.switch, name='switch'),
    path('forms/mega-option/', views.mega_option, name='mega_option'),
    path('forms/date-range-picker/', views.date_range_picker, name='date_range_picker'),
    path('forms/form-datepicker/', views.form_datepicker, name='form_datepicker'),
    path('forms/date-range-picker/', views.date_range_picker, name='date_range_picker'),
    path('forms/time-picker/', views.timepicker, name='timepicker'),
    path('forms/choices/', views.form_choices, name='form_choices'),
    path('forms/recaptcha/', views.recaptcha, name='recaptcha'),
    path('forms/input-mask/', views.input_mask, name='input_mask'),
    path('forms/clipboard/', views.clipboard, name='clipboard'),
    path('forms/nouislider/', views.nouislider, name='nouislider'),
    path('forms/bootstrap-switch/', views.bootstrap_switch, name='bootstrap_switch'),
    path('forms/typeahead/', views.typeahead, name='typeahead'),

    # Text Editors
    path('forms/tinymce/', views.tinymce, name='tinymce'),
    path('forms/quill/', views.quill, name='quill'),
    path('forms/ckeditor-classic/', views.ck_editor_classic, name='ck_editor_classic'),
    path('forms/ckeditor-document/', views.ck_editor_document, name='ck_editor_document'),
    path('forms/ckeditor-inline/', views.ck_editor_inline, name='ck_editor_inline'),
    path('forms/ckeditor-balloon/', views.ck_editor_balloon, name='ck_editor_balloon'),
    path('forms/markdown/', views.markdown, name='markdown'),

    # Form Layouts
    path('form/default-layout/', views.form_layout, name='form_layout'),
    path('form/multicolumn/', views.multicolumn, name='multicolumn'),
    path('form/action-bars/', views.action_bars, name='action_bars'),
    path('form/sticky-action-bars/', views.sticky_action_bars, name='sticky_action_bars'),

    # File Upload
    path('form/dropzone/', views.dropzone, name='dropzone'),
    path('form/uppy/', views.uppy, name='uppy'),
    path('form/form-validation/', views.form_validation, name='form_validation'),
    path('form/image-cropper/', views.image_cropper, name='image_cropper'),

    # Table
    path('table/basic-table/', views.basic_table, name='basic_table'),
    path('table/sizing-table/', views.sizing_table, name='sizing_table'),
    path('table/border-table/', views.border_table, name='border_table'),
    path('table/styling-table/', views.styling_table, name='styling_table'),

    # Vanilla Table
    path('table/basic-initialization/', views.basic_initialization, name='basic_initialization'),
    path('table/dynamic-import/', views.dynamic_import, name='dynamic_import'),
    path('table/render-column-cells/', views.render_column_cells, name='render_column_cells'),
    path('table/column-manipulation/', views.column_manipulation, name='column_manipulation'),
    path('table/datetime-sorting/', views.datetime_sorting, name='datetime_sorting'),
    path('table/methods/', views.methods, name='methods'),
    path('table/add-rows/', views.add_rows, name='add_rows'),
    path('table/fetch-api/', views.fetch_api, name='fetch_api'),
    path('table/filters/', views.filter, name='filters'),
    path('table/export/', views.export, name='export'),

    # Data Table
    path('table/advance-initialization/', views.advance_initialization, name='advance_initialization'),
    path('table/advance-styling/', views.advance_styling, name='advance_styling'),
    path('table/advance-api/', views.advance_api, name='advance_api'),
    path('table/advance-plugin/', views.advance_plugin, name='advance_plugin'),
    path('table/advance-data-source/', views.advance_data_source, name='advance_data_source'),

    # DT Extension
    path('table/autofill/', views.autofill, name='autofill'),
    path('table/basic-button/', views.basic_button, name='basic_button'),
    path('table/data-export/', views.data_export, name='data_export'),
    path('table/col-reorder/', views.col_reorder, name='col_reorder'),
    path('table/fixed-column/', views.fixed_column, name='fixed_column'),
    path('table/fixed-header/', views.fixed_header, name='fixed_header'),
    path('table/key-table/', views.key_table, name='key_table'),
    path('table/responsive/', views.autofill, name='responsive'),
    path('table/row-reorder/', views.row_reorder, name='row_reorder'),
    path('table/scroller/', views.scroller, name='scroller'),
    path('table/select-table/', views.select_table, name='select_table'),

    # Authentication

    ######## Common #########
    path('accounts/logout/', views.user_logout_view, name='logout'),
    path('accounts/password-reset-confirm-v1/<uidb64>/<token>/', 
        views.UserPasswordResetConfirmV1View.as_view(), name='password_reset_confirm'),
    path('accounts/password-reset-done-v1/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password-reset-done.html'
    ), name='password_reset_done'),
    path('accounts/password-reset-complete-v1/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password-reset-complete.html'
    ), name='password_reset_complete'),
    path('accounts/password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password-change-done.html'
    ), name="password_change_done" ),
    ######## End Common #########


    ######## v1 #########
    path('accounts/login-v1/', views.UserLoginV1View.as_view(), name='login_v1'),
    path('accounts/register-v1/', views.register_v1, name='register_v1'),
    path('accounts/password-reset-v1/', views.UserPasswordResetV1View.as_view(), name='password_reset_v1'),
    path('accounts/password-change-v1/', views.UserPasswordChangeV1View.as_view(), name='password_change_v1'),
    ######## End v1 #########


    ######## v2 #########
    path('accounts/login-v2/', views.UserLoginV2View.as_view(), name='login_v2'),
    path('accounts/register-v2/', views.register_v2, name='register_v2'),
    path('accounts/password-reset-v2/', views.UserPasswordResetV2View.as_view(), name='password_reset_v2'),
    path('accounts/password-change-v2/', views.UserPasswordChangeV2View.as_view(), name='password_change_v2'),
    ######## End v2 #########


    ######## v3 #########
    path('accounts/login-v3/', views.UserLoginV3View.as_view(), name='login_v3'),
    path('accounts/register-v3/', views.register_v3, name='register_v3'),
    path('accounts/password-reset-v3/', views.UserPasswordResetV3View.as_view(), name='password_reset_v3'),
    path('accounts/password-change-v3/', views.UserPasswordChangeV3View.as_view(), name='password_change_v3'),
    ######## End v3 #########


    path('accounts/check-mail-v1/', views.check_mail_v1, name='check_mail_v1'),
    path('accounts/check-mail-v2/', views.check_mail_v2, name='check_mail_v2'),
    path('accounts/check-mail-v3/', views.check_mail_v3, name='check_mail_v3'),
    path('accounts/reset-password-v2/', views.reset_password_v2, name='reset_password_v2'),
    path('accounts/reset-password-v3/', views.reset_password_v3, name='reset_password_v3'),
    path('accounts/code-verification-v1/', views.code_verification_v1, name='code_verification_v1'),
    path('accounts/code-verification-v2/', views.code_verification_v2, name='code_verification_v2'),
    path('accounts/code-verification-v3/', views.code_verification_v3, name='code_verification_v3'),

    # Price
    path('price/price-v1/', views.price_v1, name='price_v1'),
    path('price/price-v2/', views.price_v2, name='price_v2'),

    # Maintenance
    path('pages/error-404/', views.error_404, name='error_404'),
    path('pages/coming-soon-v1/', views.coming_soon_v1, name='coming_soon_v1'),
    path('pages/coming-soon-v2/', views.coming_soon_v2, name='coming_soon_v2'),
    path('pages/under-contruction/', views.under_construction, name='under_construction'),

    path('pages/contact-us/', views.contact_us, name='contact_us'),
    path('pages/faq/', views.faq, name='faq'),
    path('pages/privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('pages/landing/', views.landing, name='landing'),
    
    path('other/sample-page/', views.sample_page, name='sample_page'),
]
