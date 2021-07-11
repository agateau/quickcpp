# quickcpp

`quickcpp` is a small command-line tool to quickly build and run a single C++ file. Handy for quick experimentations.

## Usage

The simplest usage is `quickcpp <path/to/some/cppfile>`. When called like this, `quickcpp` builds the file (producing a `a.out` file) and runs the result.

```
$ cat examples/helloworld.cpp 
#include <iostream>

int main(int argc, char** argv) {
    std::cout << "Hello world!\n";
    return 0;
}

$ quickcpp examples/helloworld.cpp 
- Building ---------------------
c++ examples/helloworld.cpp -Wall -fPIC -std=c++17 -g
- Running ----------------------
Hello world!
```

### Using other libraries

Want to experiment something with [QtWidgets][]? You can specify any installed pkg-config compliant packages using `-p <package>`:

[QtWidgets]: https://doc.qt.io/qt-5.15/qtwidgets-index.html

```
$ cat examples/qt.cpp 
#include <QApplication>
#include <QMainWindow>

int main(int argc, char** argv) {
    QApplication app(argc, argv);

    QMainWindow window;
    window.setWindowTitle("Hello World");
    window.show();

    return app.exec();
}

$ quickcpp -p Qt5Widgets examples/qt.cpp 
- Building ---------------------
c++ examples/qt.cpp -Wall -fPIC -std=c++17 -g -DQT_WIDGETS_LIB -DQT_GUI_LIB -DQT_CORE_LIB -I/usr/include/x86_64-linux-gnu/qt5/QtWidgets -I/usr/include/x86_64-linux-gnu/qt5 -I/usr/include/x86_64-linux-gnu/qt5/QtGui -I/usr/include/x86_64-linux-gnu/qt5 -I/usr/include/x86_64-linux-gnu/qt5/QtCore -I/usr/include/x86_64-linux-gnu/qt5 -lQt5Widgets -lQt5Gui -lQt5Core
- Running ----------------------
```

You should see a window like this one:

![qt.png](examples/qt.png)

Any package listed by `pkg-config --list-all` can be used by `quickcpp`.

### Live reload

`quickcpp` can use [entr](http://entrproject.org/) to automatically rebuild and rerun your file. Just install `entr` and run `quickcpp` with the `-l` flag.

## Installation

The recommended solution is to use [pipx][]:

```
pipx install quickcpp
```

[pipx]: https://github.com/pipxproject/pipx

But you can also install it with `pip`:

```
pip install --user quickcpp
```

## License

Apache 2.0
