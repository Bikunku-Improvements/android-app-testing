# Android App Testing Tool

## Idea

This is a tool used to measure CPU and Memory.

In the perf module, there is also a few methods that provides FPS and Netstat capabilities.
We do not need the netstat capabilities, and as for the FPS, we do it manually to complete the thesis.

As for the reason why FPS is not being measured, is because it cannot actually measure it. Initially we want to use SurfaceFlinger dump to get the data from the rendered surface. But, as of Android 8, this dump has been protected and cannot be measured unless we actually root the phone.

You can see it being documented here _very implicitly_ in this repo: https://github.com/alibaba/mobileperf/blob/master/mobileperf/android/fps.py. On method `_collector_thread`, in Chinese.

Alternatively, you can use `dumpsys gfxinfo` to measure the frames that are rendered by your app. But, for this thesis, we need to measure Google Chrome's frame. Unfortunately, there are no useful data when we do `dumpsys gfxinfo` to Google Chrome.

There's an interesting thesis that are made by Camille Fournier: https://www.diva-portal.org/smash/get/diva2:1474729/FULLTEXT01.pdf

If you read into this, there could be tool that can measure the app's FPS through systrace. But, as of 2022, they do not ship it through Android SDK's platform tools. And the only way to actually mimic the systrace is through AGI ([gpuinspector.dev](https://gpuinspector.dev)). When we wanted to use AGI, we do not have the [devices that are capable of supporting AGI](https://developer.android.com/agi/supported-devices).

Fortunately, we can measure this using Samsung's natively shipped app, GPUWatch. With this, we can measure FPS, but we need to calculate it manually. Our guess is because GPUWatch is shipped natively, they have access to the API given by Android that access SurfaceFlinger's data.

## Inspired by:

- pure-python-adb: https://github.com/Swind/pure-python-adb
- Uiautomator2's perf module: https://github.com/openatx/uiautomator2/tree/master/uiautomator2/ext/perf
