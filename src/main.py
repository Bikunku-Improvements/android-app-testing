import uiautomator2 as u2
import uiautomator2.ext.perf as perf

package_name = 'com.android.chrome'


def main():
    d = u2.connect('RR8NA05A0FP')
    print(d.info)


if __name__ == "__main__":
    main()
