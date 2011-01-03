from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('users.views',
    url(r"^login/?$", "login.login", name="login"),
    url(r"^logout/?$", "login.logout", name="logout"),
    url(r"^registration/?$", "registration.registration", name="registration"),
    url(r"^registration/confirm/?$", "registration.confirm", name="registration_confirm"),
    url(r"^registration/resend/?$", "registration.resend", name="registration_resend"),
    url(r"^reset-password/?$", "reset_password.init", name="reset_password_init"),
    url(r"^reset-password/(?P<key>[^/]+)/?$", "reset_password.reset_password", name="reset_password"),
    url(r"^profile/?$", "profile.profile", name="profile"),
)
