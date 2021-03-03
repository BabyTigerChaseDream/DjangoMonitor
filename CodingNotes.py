# parse html structure from r.response content (webpage.html)
>>> from lxml import html
>>> tree = html.fromstring(r.content)

>>> type(tree.xpath("//a"))
<class 'list'>

>>> href=tree.xpath("//a")[3]
>>> len(tree.xpath("//a"))
13
>>> for l in tree.xpath("//a"):
...     print(l.get("href"))
... 
https://android-crashes.prod.booking.com/
https://android-crashes.prod.booking.com/crash/
https://android-crashes.prod.booking.com/crash/android
https://android-crashes.prod.booking.com/crash/pulse-android
https://android-crashes.prod.booking.com/crash/ios
https://android-crashes.prod.booking.com/crash/daily/2021-01-28/android

# Get crash ID:
version_url = 'https://android-crashes.prod.booking.com/crash/report/2021-02-09/25.9-all/android/page/1'
>>> for c in tree_version.xpath("//div[@class='panel panel-primary crash-item active-crash-panel']"):
...     print(c)

divlist=[c for c in tree_version.xpath("//div[@class='panel panel-primary crash-item active-crash-panel']")]

>>> type(divlist[0])
<class 'lxml.html.HtmlElement'>
>>> divlist[0].get('id')
'crash-5518818'

# Get a list of "Crash keys"
# directly get from main version_url
>>> tree_version.xpath("//pre[@class='stacktrace']")[0].get('id')
'crash-trace-5518818'
>>> tree_version.xpath("//pre[@class='stacktrace']")[2].get('id')
'crash-trace-5528758'
>>> tree_version.xpath("//pre[@class='stacktrace']")[2].text_content()
"java.lang.NoSuchMethodError: No direct method (Lcom/booking/payment/component/ui/customization/UiCustomization$Background;Lcom/booking/payment/component/ui/customization/UiCustomization$Divider;Lcom/booking/payment/component/ui/customization/UiCustomization$Header;Lcom/booking/payment/component/ui/customization/UiCustomization$PaymentIcons;Lcom/booking/payment/component/ui/customization/UiCustomization$NavigationBar;Lcom/booking/payment/component/ui/customization/UiCustomization$Text;ILkotlin/jvm/internal/DefaultConstructorMarker;)V in class Lcom/booking/payment/component/ui/customization/UiCustomization; or its super classes (declaration of 'com.booking.payment.component.ui.customization.UiCustomization' appears in base.apk:classes11.dex)\n  at com.booking.android.payment.payin.timing.PaymentManager.setupPaymentView(PaymentManager.kt:3)\n  at com.booking.android.payment.payin.timing.PaymentManager.setup(PaymentManager.kt:13)\n  at com.booking.reservationmanager.manager.ReservationManager.processInitState(ReservationManager.kt:42)\n  at com.booking.reservationmanager.network.ReservationNetworkHelper$callInitCheckout$1.onResponse(ReservationNetworkHelper.kt:27)\n  at retrofit2.-$$Lambda$DefaultCallAdapterFactory$ExecutorCallbackCall$1$hVGjmafRi6VitDIrPNdoFizVAdk.run(lambda:3)\n  at android.os.Handler.handleCallback(Handler.java:761)  at android.os.Handler.dispatchMessage(Handler.java:98)  at android.os.Looper.loop(Looper.java:156)  at android.app.ActivityThread.main(ActivityThread.java:6523)  at java.lang.reflect.Method.invoke(Native Method)  at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:942)  at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:832)"

############ Get 'NEW' keyword ############
version_level_url = 'https://android-crashes.prod.booking.com/crash/report/2021-02-23/26.1/android/page/1'

#### show new crashes only ####
# NOT precise ...
filter_new_crashes='https://android-crashes.prod.booking.com/crash/report/2021-02-09/25.9?show_new=show-only'

# Make a crash ID pool 
# iterate all new ID based on previous ones
# Locate: 'table-center' in 
# 'https://android-crashes.prod.booking.com/crash/'

# TODO: Get a single crash session data from "crash ID"

