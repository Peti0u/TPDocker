from django.shortcuts import render, redirect
from admin_berry_pro.forms import LoginForm, RegistrationForm, UserPasswordResetForm, UserSetPasswordForm, UserPasswordChangeForm
from django.contrib.auth import logout

from django.contrib.auth import views as auth_views

# Create your views here.

def index(request):
  return render(request, 'pages/index.html')

# Dashboard
def default(request):
  return render(request, 'pages/dashboard/index.html')

def analytics(request):
  return render(request, 'pages/dashboard/analytics.html')

# Widgets
def statistics(request):
  return render(request, 'pages/widgets/statistics.html')

def data(request):
  return render(request, 'pages/widgets/data.html')

def chart(request):
  return render(request, 'pages/widgets/chart.html')

# Layout
def vertical_layout(request):
  return render(request, 'pages/demo/layout-vertical.html')

def horizontal_layout(request):
  return render(request, 'pages/demo/layout-horizontal.html')

def compact_layout(request):
  return render(request, 'pages/demo/layout-compact.html')

# Application
def social_profile(request):
  return render(request, 'pages/application/social-profile.html')

# Account
def account_profile_v1(request):
  return render(request, 'pages/application/account-profile-v1.html')

def account_profile_v2(request):
  return render(request, 'pages/application/account-profile-v2.html')

def account_profile_v3(request):
  return render(request, 'pages/application/account-profile-v3.html')

# Card
def user_card_v1(request):
  return render(request, 'pages/application/user-card-v1.html')

def user_card_v2(request):
  return render(request, 'pages/application/user-card-v2.html')

def user_card_v3(request):
  return render(request, 'pages/application/user-card-v3.html')

# List
def user_list_v1(request):
  return render(request, 'pages/application/user-list-v1.html')

def user_list_v2(request):
  return render(request, 'pages/application/user-list-v2.html')

# Customer
def customer_list(request):
  return render(request, 'pages/application/cust_customer_list.html')

def order_list(request):
  return render(request, 'pages/application/cust_order_list.html')

def create_invoice(request):
  return render(request, 'pages/application/cust_create_invoice.html')

def order_details(request):
  return render(request, 'pages/application/cust_order_details.html')

def product_list(request):
  return render(request, 'pages/application/cust_product_list.html')

def product_review(request):
  return render(request, 'pages/application/cust_product_review.html')

def chat(request):
  return render(request, 'pages/application/chat.html')

def kanban(request):
  return render(request, 'pages/application/kanban.html')

def mail(request):
  return render(request, 'pages/application/mail.html')

def calendar(request):
  return render(request, 'pages/application/calendar.html')

def contact_cards(request):
  return render(request, 'pages/application/contact_cards.html')

def contact_list(request):
  return render(request, 'pages/application/contact_list.html')

# Ecommerce
def ecom_product(request):
  return render(request, 'pages/application/ecom_product.html')

def ecom_product_details(request):
  return render(request, 'pages/application/ecom_product-details.html')

def ecom_product_list(request):
  return render(request, 'pages/application/ecom_product-list.html')

def ecom_checkout(request):
  return render(request, 'pages/application/ecom_checkout.html')
  
# Basic Elements
def alerts(request):
  return render(request, 'pages/elements/bc_alert.html')

def badges(request):
  return render(request, 'pages/elements/bc_badges.html')

def breadcrumb_pagination(request):
  return render(request, 'pages/elements/bc_breadcrumb-pagination.html')

def button(request):
  return render(request, 'pages/elements/bc_button.html')

def card(request):
  return render(request, 'pages/elements/bc_card.html')

def carousel(request):
  return render(request, 'pages/elements/bc_carousel.html')

def collapse(request):
  return render(request, 'pages/elements/bc_collapse.html')

def color(request):
  return render(request, 'pages/elements/bc_color.html')

def dropdowns(request):
  return render(request, 'pages/elements/bc_dropdowns.html')

def extra(request):
  return render(request, 'pages/elements/bc_extra.html')

def grid(request):
  return render(request, 'pages/elements/bc_grid.html')

def list_group(request):
  return render(request, 'pages/elements/bc_list-group.html')

def modal(request):
  return render(request, 'pages/elements/bc_modal.html')

def offcanvas(request):
  return render(request, 'pages/elements/bc_offcanvas.html')

def progress(request):
  return render(request, 'pages/elements/bc_progress.html')

def spinner(request):
  return render(request, 'pages/elements/bc_spinner.html')

def tabs(request):
  return render(request, 'pages/elements/bc_tabs.html')

def toasts(request):
  return render(request, 'pages/elements/bc_toasts.html')

def tooltip_popover(request):
  return render(request, 'pages/elements/bc_tooltip-popover.html')

def typography(request):
  return render(request, 'pages/elements/bc_typography.html')


# Advance Elements
def sweet_alert(request):
  return render(request, 'pages/elements/ac_alert.html')

def datepicker(request):
  return render(request, 'pages/elements/ac_datepicker-componant.html')

def lightbox(request):
  return render(request, 'pages/elements/ac_lightbox.html')

def ac_modal(request):
  return render(request, 'pages/elements/ac_modal.html')

def notification(request):
  return render(request, 'pages/elements/ac_notification.html')

def range_slider(request):
  return render(request, 'pages/elements/ac_rangeslider.html')

def slider(request):
  return render(request, 'pages/elements/ac_slider.html')

def syntax_highlighter(request):
  return render(request, 'pages/elements/ac_syntax_highlighter.html')

def tour(request):
  return render(request, 'pages/elements/ac_tour.html')

def tree_view(request):
  return render(request, 'pages/elements/ac_treeview.html')

# Icons
def feather(request):
  return render(request, 'pages/elements/icon-feather.html')

def font_awesome(request):
  return render(request, 'pages/elements/icon-fontawesome.html')

def material(request):
  return render(request, 'pages/elements/icon-material.html')

def tabler(request):
  return render(request, 'pages/elements/icon-tabler.html')

# Forms
def form_elements(request):
  return render(request, 'pages/forms/form_elements.html')

def form_floating(request):
  return render(request, 'pages/forms/form_floating.html')

def form_options(request):
  return render(request, 'pages/forms/form2_basic.html')

def input_groups(request):
  return render(request, 'pages/forms/form2_input_group.html')

def checkbox(request):
  return render(request, 'pages/forms/form2_checkbox.html')

def radio(request):
  return render(request, 'pages/forms/form2_radio.html')

def switch(request):
  return render(request, 'pages/forms/form2_switch.html')

def mega_option(request):
  return render(request, 'pages/forms/form2_megaoption.html')

def form_datepicker(request):
  return render(request, 'pages/forms/form2_datepicker.html')

def date_range_picker(request):
  return render(request, 'pages/forms/form2_daterangepicker.html')

def timepicker(request):
  return render(request, 'pages/forms/form2_timepicker.html')

def form_choices(request):
  return render(request, 'pages/forms/form2_choices.html')

def recaptcha(request):
  return render(request, 'pages/forms/form2_recaptcha.html')

def input_mask(request):
  return render(request, 'pages/forms/form2_inputmask.html')

def clipboard(request):
  return render(request, 'pages/forms/form2_clipboard.html')

def nouislider(request):
  return render(request, 'pages/forms/form2_nouislider.html')

def bootstrap_switch(request):
  return render(request, 'pages/forms/form2_switchjs.html')

def typeahead(request):
  return render(request, 'pages/forms/form2_typeahead.html')

# Text Editors
def tinymce(request):
  return render(request, 'pages/forms/form2_tinymce.html')

def quill(request):
  return render(request, 'pages/forms/form2_quill.html')

def ck_editor_classic(request):
  return render(request, 'pages/forms/editor-classic.html')

def ck_editor_document(request):
  return render(request, 'pages/forms/editor-document.html')

def ck_editor_inline(request):
  return render(request, 'pages/forms/editor-inline.html')

def ck_editor_balloon(request):
  return render(request, 'pages/forms/editor-balloon.html')

def markdown(request):
  return render(request, 'pages/forms/form2_markdown.html')

# Form Layout
def form_layout(request):
  return render(request, 'pages/forms/form2_lay-default.html')

def multicolumn(request):
  return render(request, 'pages/forms/form2_lay-multicolumn.html')

def action_bars(request):
  return render(request, 'pages/forms/form2_lay-actionbars.html')

def sticky_action_bars(request):
  return render(request, 'pages/forms/form2_lay-stickyactionbars.html')

# File Upload
def dropzone(request):
  return render(request, 'pages/forms/file-upload.html')

def uppy(request):
  return render(request, 'pages/forms/form2_flu-uppy.html')

def form_validation(request):
  return render(request, 'pages/forms/form-validation.html')

def image_cropper(request):
  return render(request, 'pages/forms/image_crop.html')

# Table
def basic_table(request):
  return render(request, 'pages/table/tbl_bootstrap.html')

def sizing_table(request):
  return render(request, 'pages/table/tbl_sizing.html')

def border_table(request):
  return render(request, 'pages/table/tbl_border.html')

def styling_table(request):
  return render(request, 'pages/table/tbl_styling.html')

# Vanilla Table
def basic_initialization(request):
  return render(request, 'pages/table/tbl_dt-simple.html')

def dynamic_import(request):
  return render(request, 'pages/table/tbl_dt-dynamic-import.html')

def render_column_cells(request):
  return render(request, 'pages/table/tbl_dt-render-column-cells.html')

def column_manipulation(request):
  return render(request, 'pages/table/tbl_dt-column-manipulation.html')

def datetime_sorting(request):
  return render(request, 'pages/table/tbl_dt-datetime-sorting.html')

def methods(request):
  return render(request, 'pages/table/tbl_dt-methods.html')

def add_rows(request):
  return render(request, 'pages/table/tbl_dt-add-rows.html')

def fetch_api(request):
  return render(request, 'pages/table/tbl_dt-fetch-api.html')

def filter(request):
  return render(request, 'pages/table/tbl_dt-filters.html')

def export(request):
  return render(request, 'pages/table/tbl_dt-export.html')

# Data Table
def advance_initialization(request):
  return render(request, 'pages/table/dt_advance.html')

def advance_styling(request):
  return render(request, 'pages/table/dt_styling.html')

def advance_api(request):
  return render(request, 'pages/table/dt_api.html')

def advance_plugin(request):
  return render(request, 'pages/table/dt_plugin.html')

def advance_data_source(request):
  return render(request, 'pages/table/dt_sources.html')

# DT Extension
def autofill(request):
  return render(request, 'pages/table/dt_ext_autofill.html')

def basic_button(request):
  return render(request, 'pages/table/dt_ext_basic_buttons.html')

def data_export(request):
  return render(request, 'pages/table/dt_ext_export_buttons.html')

def col_reorder(request):
  return render(request, 'pages/table/dt_ext_col_reorder.html')

def fixed_column(request):
  return render(request, 'pages/table/dt_ext_fixed_columns.html')

def fixed_header(request):
  return render(request, 'pages/table/dt_ext_fixed_header.html')

def key_table(request):
  return render(request, 'pages/table/dt_ext_key_table.html')

def responsive(request):
  return render(request, 'pages/table/dt_ext_responsive.html')

def row_reorder(request):
  return render(request, 'pages/table/dt_ext_row_reorder.html')

def row_recorder(request):
  return render(request, 'pages/table/dt_ext_row_recorder.html')

def scroller(request):
  return render(request, 'pages/table/dt_ext_scroller.html')

def select_table(request):
  return render(request, 'pages/table/dt_ext_select.html')

# Authentication

######## Start v1 #########
def register_v1(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print('Account created successfully!')
      return redirect('/accounts/login-v1/')
    else:
      print("Registration failed!")
  else:
    form = RegistrationForm()
  
  context = {'form': form}
  return render(request, 'accounts/register-v1.html', context)

class UserLoginV1View(auth_views.LoginView):
  template_name = 'accounts/login-v1.html'
  form_class = LoginForm
  success_url = '/dashboard'

class UserPasswordChangeV1View(auth_views.PasswordChangeView):
  template_name = 'accounts/password-change-v1.html'
  form_class = UserPasswordChangeForm

class UserPasswordResetV1View(auth_views.PasswordResetView):
  template_name = 'accounts/forgot-password-v1.html'
  form_class = UserPasswordResetForm

######## End v1 #########


######## Start v2 #########
def register_v2(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print('Account created successfully!')
      return redirect('/accounts/login-v2/')
    else:
      print("Registration failed!")
  else:
    form = RegistrationForm()
  
  context = {'form': form}
  return render(request, 'accounts/register-v2.html', context)

class UserLoginV2View(auth_views.LoginView):
  template_name = 'accounts/login-v2.html'
  form_class = LoginForm
  success_url = '/dashboard'

class UserPasswordChangeV2View(auth_views.PasswordChangeView):
  template_name = 'accounts/password-change-v2.html'
  form_class = UserPasswordChangeForm

class UserPasswordResetV2View(auth_views.PasswordResetView):
  template_name = 'accounts/forgot-password-v2.html'
  form_class = UserPasswordResetForm

######## End v2 #########


######## Start v3 #########
def register_v3(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      form.save()
      print('Account created successfully!')
      return redirect('/accounts/login-v3/')
    else:
      print("Registration failed!")
  else:
    form = RegistrationForm()
  
  context = {'form': form}
  return render(request, 'accounts/register-v3.html', context)

class UserLoginV3View(auth_views.LoginView):
  template_name = 'accounts/login-v3.html'
  form_class = LoginForm
  success_url = '/dashboard'

class UserPasswordChangeV3View(auth_views.PasswordChangeView):
  template_name = 'accounts/password-change-v3.html'
  form_class = UserPasswordChangeForm

class UserPasswordResetV3View(auth_views.PasswordResetView):
  template_name = 'accounts/forgot-password-v3.html'
  form_class = UserPasswordResetForm

######## End v3 #########


######## Common #########
class UserPasswordResetConfirmV1View(auth_views.PasswordResetConfirmView):
  template_name = 'accounts/reset-password-v1.html'
  form_class = UserSetPasswordForm

def user_logout_view(request):
  logout(request)
  return redirect('/accounts/login-v1/')

######## End Common #########


def check_mail_v1(request):
  return render(request, 'accounts/check-mail-v1.html')

def check_mail_v2(request):
  return render(request, 'accounts/check-mail-v2.html')

def check_mail_v3(request):
  return render(request, 'accounts/check-mail-v3.html')

def reset_password_v2(request):
  return render(request, 'accounts/reset-password-v2.html')

def reset_password_v3(request):
  return render(request, 'accounts/reset-password-v3.html')

def code_verification_v1(request):
  return render(request, 'accounts/code-verification-v1.html')

def code_verification_v2(request):
  return render(request, 'accounts/code-verification-v2.html')

def code_verification_v3(request):
  return render(request, 'accounts/code-verification-v3.html')

# Price
def price_v1(request):
  return render(request, 'accounts/price-v1.html')

def price_v2(request):
  return render(request, 'accounts/price-v2.html')

# Maintenance
def error_404(request):
  return render(request, 'accounts/error-404.html')

def coming_soon_v1(request):
  return render(request, 'accounts/coming-soon-v1.html')

def coming_soon_v2(request):
  return render(request, 'accounts/coming-soon-v2.html')

def under_construction(request):
  return render(request, 'accounts/under-construction.html')

def contact_us(request):
  return render(request, 'accounts/contact-us.html')

def faq(request):
  return render(request, 'accounts/faq.html')

def privacy_policy(request):
  return render(request, 'accounts/privacy-policy.html')

def landing(request):
  return render(request, 'accounts/landing.html')

def sample_page(request):
  return render(request, 'pages/other/sample-page.html')