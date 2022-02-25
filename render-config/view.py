# from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QSpinBox
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QWidget

import json
import toml
import sys

FRANGE = [1001, 1240, 1]
PICTURE = "$HIP/render/$HIPNAME.$OS.$FRANGE4.exr"
CAMERA = "/cameras/camera1"
RESOLUTION = [1280, 720]

GENERIC_LABEL_WIDTH = 120


class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__()
        self.setWindowTitle("Karma")
        self.setFixedWidth(700)
        self.glayout()
        self.show()

    def glayout(self):
        layout = QVBoxLayout()

        layout.addLayout(self.buttons())
        layout.addLayout(self.frangeLayout())
        layout.addWidget(QLabel("Common Settings"))
        layout.addLayout(self.pictureLayout())
        layout.addLayout(self.cameraLayout())
        layout.addLayout(self.resolutionLayout())
        # layout.addLayout(self.engineLayout())
        self.engine = self.orderedMenu(
            layout, "Rendering Engine", ["CPU Engine", "XPU Engine (Alpha)"]
        )
        self.samplesperpixel = self.intSlider(layout, "Pixel Samples", 9)

        tabs = QTabWidget()
        tabs.addTab(self.renderingTab(), "Rendering")
        tabs.addTab(self.imageOutputTab(), "Image Output")
        tabs.addTab(self.deepOutputTab(), "Deep Output")
        tabs.addTab(self.advancedTab(), "Advanced")
        layout.addWidget(tabs)

        self.setLayout(layout)

    def buttons(self):
        render_buttons_layout = QHBoxLayout()
        execute = QPushButton()
        execute.setText("Save")
        execute.clicked.connect(self.save)

        render_buttons_layout.addWidget(execute)

        return render_buttons_layout

    def frangeLayout(self):
        frange_layout = QHBoxLayout()
        frange_label = QLabel("Start/End/Inc")
        frange_label.setFixedWidth(GENERIC_LABEL_WIDTH)

        start, end, inc = FRANGE

        self.frange_start = QSpinBox()
        self.frange_start.setMaximum(1000000)
        self.frange_start.setValue(start)

        self.frange_end = QSpinBox()
        self.frange_end.setMaximum(1000000)
        self.frange_end.setValue(end)

        self.frange_inc = QSpinBox()
        self.frange_inc.setValue(inc)

        frange_layout.addWidget(frange_label)
        frange_layout.addWidget(self.frange_start)
        frange_layout.addWidget(self.frange_end)
        frange_layout.addWidget(self.frange_inc)

        return frange_layout

    def pictureLayout(self):
        picture_layout = QHBoxLayout()
        picture_label = QLabel("Output Picture")
        picture_label.setFixedWidth(GENERIC_LABEL_WIDTH)

        self.picture = QLineEdit()
        self.picture.setText(PICTURE)

        picture_layout.addWidget(picture_label)
        picture_layout.addWidget(self.picture)

        return picture_layout

    def cameraLayout(self):
        camera_layout = QHBoxLayout()
        camera_label = QLabel("Camera")
        camera_label.setFixedWidth(GENERIC_LABEL_WIDTH)

        self.camera = QLineEdit()
        self.camera.setText(CAMERA)

        camera_layout.addWidget(camera_label)
        camera_layout.addWidget(self.camera)

        return camera_layout

    def resolutionLayout(self):
        resolution_layout = QHBoxLayout()
        resolution_label = QLabel("Resolution")
        resolution_label.setFixedWidth(GENERIC_LABEL_WIDTH)

        resx, resy = RESOLUTION

        self.resolutionx = QSpinBox()
        self.resolutionx.setMaximum(1000000)
        self.resolutionx.setValue(resx)

        self.resolutiony = QSpinBox()
        self.resolutiony.setMaximum(1000000)
        self.resolutiony.setValue(resy)

        resolution_layout.addWidget(resolution_label)
        resolution_layout.addWidget(self.resolutionx)
        resolution_layout.addWidget(self.resolutiony)

        return resolution_layout

    def renderingTab(self):
        rendering_tab = QWidget()
        layout = QVBoxLayout()

        tabs = QTabWidget()
        tabs.addTab(self._samplingTab(), "Sampling")
        tabs.addTab(self._limitsTab(), "Limits")
        layout.addWidget(tabs)

        rendering_tab.setLayout(layout)
        return rendering_tab

    def _samplingTab(self):
        sampling_tab = QWidget()
        layout = QVBoxLayout()

        self.convergencemode = self.orderedMenu(
            layout, "Convergence Mode", ["Variance"]
        )
        self.minraysamples = self.intSlider(layout, "Min Ray Samples", 1)
        self.maxraysamples = self.intSlider(layout, "Max Ray Samples", 9)
        layout.addWidget(QLabel("Lights Quality"))
        self.lightsamplingmode = self.orderedMenu(
            layout, "Light Sampling Mode", ["Light Tree"]
        )
        self.lightsamplingquality = self.intSlider(layout, "Light Sampling Quality", 1)

        sampling_tab.setLayout(layout)
        return sampling_tab

    def _limitsTab(self):
        limits_tab = QWidget()
        layout = QVBoxLayout()

        self.diffuselimit = self.intSlider(layout, "Diffuse Limit", 1)
        self.reflectionlimit = self.intSlider(layout, "Reflection Limit", 4)
        self.refractionlimit = self.intSlider(layout, "Refraction Limit", 4)
        self.volumelimit = self.intSlider(layout, "Volume Limit", 0)
        self.ssslimit = self.intSlider(layout, "SSS Limit", 0)
        self.colorlimit = self.intSlider(layout, "Color Limit", 10)

        limits_tab.setLayout(layout)
        return limits_tab

    def intSlider(self, parent_layout, label, value):
        layout = QHBoxLayout()
        slider_label = QLabel(label)
        slider_label.setFixedWidth(GENERIC_LABEL_WIDTH)
        slider = QSpinBox()
        slider.setValue(value)
        layout.addWidget(slider_label)
        layout.addWidget(slider)
        parent_layout.addLayout(layout)
        return slider

    def orderedMenu(self, parent_layout, label, list_):
        layout = QHBoxLayout()
        menu_label = QLabel(label)
        menu_label.setFixedWidth(GENERIC_LABEL_WIDTH)
        menu = QComboBox()
        menu.addItems(list_)
        layout.addWidget(menu_label)
        layout.addWidget(menu)
        parent_layout.addLayout(layout)
        return menu

    def imageOutputTab(self):
        image_output_tab = QWidget()
        layout = QVBoxLayout()
        image_output_tab.setLayout(layout)
        return image_output_tab

    def deepOutputTab(self):
        deep_output_tab = QWidget()
        layout = QVBoxLayout()
        deep_output_tab.setLayout(layout)
        return deep_output_tab

    def advancedTab(self):
        advanced_tab = QWidget()
        layout = QVBoxLayout()
        advanced_tab.setLayout(layout)
        return advanced_tab

    def createDict(self):
        output = {
            "frange": [
                int(self.frange_start.value()),
                int(self.frange_end.value()),
                int(self.frange_inc.value()),
            ],
            "picture": self.picture.text(),
            "camera": self.camera.text(),
            "resolution": [self.resolutionx.value(), self.resolutiony.value()],
            "engine": self.engine.currentText(),
            "samplesperpixel": self.samplesperpixel.value(),
            "rendering": {
                "sampling": {
                    "convergencemode": self.convergencemode.currentText(),
                    "minraysamples": self.minraysamples.value(),
                    "maxraysamples": self.maxraysamples.value(),
                    "lightsamplingmode": self.lightsamplingmode.currentText(),
                    "lightsamplingquality": self.lightsamplingquality.value(),
                },
                "limits": {
                    "diffuselimit": self.diffuselimit.value(),
                    "reflectionlimit": self.reflectionlimit.value(),
                    "refractionlimit": self.refractionlimit.value(),
                    "volumelimit": self.volumelimit.value(),
                    "ssslimit": self.ssslimit.value(),
                    "colorlimit": self.colorlimit.value(),
                },
            },
        }

        return output

    def save(self):
        output = self.createDict()
        with open("output.toml", "w") as fp:
            toml.dump(output, fp)
        with open("output.json", "w") as fp:
            json.dump(output, fp, indent=4)


def show():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


if __name__ == "__main__":
    show()
