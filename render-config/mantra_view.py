from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel
from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QLineEdit, QTabWidget
from PyQt5.QtWidgets import QComboBox, QSpinBox, QCheckBox, QSlider

import json
import toml
import sys

FRANGE = [1001, 1240, 1]
CAMERA = "/obj/cam1"
RESOLUTION = [1280, 720]
RENDERENGINE = [
	"Micropolygon Rendering", "Ray Tracing",
	"Micropolygon Physically Based Rendering",
	"Physically Based Rendering", "Photon Map Generation"
]

GENERIC_LABEL_WIDTH = 120

class Window(QWidget):
	def __init__(self):
		super(Window, self).__init__()
		self.setWindowTitle("Mantra")
		self.layout()
		self.show()

	def layout(self):
		layout = QVBoxLayout()		

		layout.addLayout(self.saveButton())
		layout.addLayout(self.frangeLayout())
		self.camera = self.lineEdit(layout, "Camera", "/obj/cam1")

		tabs = QTabWidget()
		tabs.addTab(self._imagesTab(), "Images")
		tabs.addTab(self._renderingTab(), "Rendering")
		layout.addWidget(tabs)

		self.setLayout(layout)

	def saveButton(self):
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
	
	def _imagesTab(self):
		images_tab = QWidget()
		layout = QVBoxLayout()

		self.vm_picture = self.lineEdit(layout, "Output Picture", "$HIP/render/$HIPNAME.$OS.$F4.exr")

		tabs = QTabWidget()
		tabs.addTab(self.__outputTab(), "Output")

		layout.addWidget(tabs)

		images_tab.setLayout(layout)
		return images_tab

	def __outputTab(self):
		output_tab = QWidget()
		layout = QVBoxLayout()

		self.vm_pfilter = self.lineEdit(layout, "Pixel Filter", "gaussian -w 2")

		output_tab.setLayout(layout)
		return output_tab

	def _renderingTab(self):
		rendering_tab = QWidget()
		layout = QVBoxLayout()

		self.vm_renderengine = self.orderedMenu(layout, "Render Engine", RENDERENGINE, 3)

		self.vm_dof = QCheckBox()
		self.vm_dof.setText("Enable Depth of Field")
		layout.addWidget(self.vm_dof)

		self.allowmotionblur = QCheckBox()
		self.allowmotionblur.setText("Allow Motion Blur")
		layout.addWidget(self.allowmotionblur)

		tabs = QTabWidget()
		tabs.addTab(self.__samplingTab(), "Sampling")
		tabs.addTab(self.__limitsTab(), "Limits")
		layout.addWidget(tabs)

		rendering_tab.setLayout(layout)
		return rendering_tab

	def __samplingTab(self):
		sampling_tab = QWidget()
		layout = QVBoxLayout()

		layout.addLayout(self.__samplesLayout())

		sampling_tab.setLayout(layout)
		return sampling_tab

	def __samplesLayout(self):
		samples_layout = QHBoxLayout()
		samples_label = QLabel("Pixel Samples")
		self.vm_samplesx = QSpinBox()
		self.vm_samplesx.setValue(3)
		self.vm_samplesy = QSpinBox()
		self.vm_samplesy.setValue(3)
		samples_layout.addWidget(samples_label)
		samples_layout.addWidget(self.vm_samplesx)
		samples_layout.addWidget(self.vm_samplesy)
		return samples_layout

	def __limitsTab(self):
		limits_tab = QWidget()
		layout = QVBoxLayout()

		self.vm_reflectlimit = self.intSlider(layout, "Reflect Limit", 10, 0, 10)
		self.vm_refractlimit = self.intSlider(layout, "Refract Limit", 10, 0, 10)
		self.vm_diffuselimit = self.intSlider(layout, "Diffuse Limit", 0, 0, 10)
		self.vm_ssslimit = self.intSlider(layout, "SSS Limit", 0, 0, 10)
		self.vm_volumelimit = self.intSlider(layout, "Volume Limit", 0, 0, 10)
		self.vm_opacitylimit = self.floatSlider(layout, "Opacity Limit", 0.995, 0.0, 1.0)
		self.vm_colorlimit = self.floatSlider(layout, "Color Limit", 10.0, 0.0, 20.0)

		limits_tab.setLayout(layout)
		return limits_tab

	# UI PRESETS

	def intSlider(self, parent_layout, label, value, min_, max_):
		layout = QHBoxLayout()
		slider_label = QLabel(label)
		slider_label.setFixedWidth(GENERIC_LABEL_WIDTH)
		slider = QSlider(Qt.Horizontal)

		slider.setMinimum(min_)
		slider.setMaximum(max_)
		slider.setValue(value)

		layout.addWidget(slider_label)
		layout.addWidget(slider)

		parent_layout.addLayout(layout)

		return slider.value()

	def floatSlider(self, parent_layout, label, value, min_, max_):
		layout = QHBoxLayout()
		slider_label = QLabel(label)
		slider_label.setFixedWidth(GENERIC_LABEL_WIDTH)
		slider = QSlider(Qt.Horizontal)

		scale = 1000

		scaled_value = int(value * scale)
		scaled_min = int(min_ * scale)
		scaled_max = int(max_ * scale)

		slider.setMinimum(scaled_min)
		slider.setMaximum(scaled_max)
		slider.setValue(scaled_value)

		layout.addWidget(slider_label)
		layout.addWidget(slider)

		parent_layout.addLayout(layout)

		return slider

	def orderedMenu(self, parent_layout, label, list_, current_index):
		layout = QHBoxLayout()
		menu_label = QLabel(label)
		menu_label.setFixedWidth(GENERIC_LABEL_WIDTH)
		menu = QComboBox()
		menu.addItems(list_)
		menu.setCurrentIndex(current_index)
		layout.addWidget(menu_label)
		layout.addWidget(menu)
		parent_layout.addLayout(layout)
		return menu

	def lineEdit(self, parent_layout, label, text):
		layout = QHBoxLayout()
		line_label = QLabel(label)
		line_label.setFixedWidth(GENERIC_LABEL_WIDTH)
		line = QLineEdit()
		line.setText(text)
		layout.addWidget(line_label)
		layout.addWidget(line)
		parent_layout.addLayout(layout)
		return line
	
	# OUTPUT AREA

	def createDict(self):
		output = {
			"frange": [
				self.frange_start.value(),
				self.frange_end.value(),
				self.frange_inc.value()
			],
			"camera": self.camera.text(),
			"image": {
				"vm_picture": self.vm_picture.text(),
				"output": {
					"vm_pfilter": self.vm_pfilter.text()
				}
			},
			"rendering": {
				"vm_renderengine": self.vm_renderengine.currentText(),
				"vm_dof": self.vm_dof.isChecked(),
				"allowmotionblur": self.allowmotionblur.isChecked(),
				"sampling": {
					"vm_samples": [
						self.vm_samplesx.value(),
						self.vm_samplesy.value()
					]
				},
				"limits": {
					"vm_reflectlimit": self.vm_reflectlimit,
					"vm_refractlimit": self.vm_refractlimit,
					"vm_diffuselimit": self.vm_diffuselimit,
					"vm_ssslimit": self.vm_ssslimit,
					"vm_volumelimit": self.vm_volumelimit,
					"vm_opacitylimit": self.vm_opacitylimit.value() * 0.001,
					"vm_colorlimit": self.vm_colorlimit.value() * 0.001
				}
			}
		}

		return output

	def save(self):
		output = self.createDict()
		with open("mantra_output.toml", "w") as fp:
			toml.dump(output, fp)
		with open("mantra_output.json", "w") as fp:
			json.dump(output, fp, indent=4)

def show():
	app = QApplication(sys.argv)
	window = Window()
	sys.exit(app.exec_())

if __name__ == '__main__':
	show()