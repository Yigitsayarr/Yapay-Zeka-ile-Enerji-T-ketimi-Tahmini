import sys
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton,
QLabel, QFileDialog, QInputDialog
from PyQt6.QtCore import Qt
from datetime import datetime, timedelta
import random
class EnergyConsumptionPredictor(QWidget):
def __init__(self):
super().__init__()
self.setWindowTitle("Energy Consumption Predictor")
self.setGeometry(100, 100, 600, 400)
self.layout = QVBoxLayout()
self.setLayout(self.layout)
self.load_button = QPushButton("Load Data")
self.load_button.clicked.connect(self.load_data)
self.layout.addWidget(self.load_button)
self.predict_button = QPushButton("Predict")
44
self.predict_button.clicked.connect(self.predict)
self.layout.addWidget(self.predict_button)
self.label = QLabel("No data loaded.")
self.layout.addWidget(self.label)
self.data = None
self.model = None
def load_data(self):
file_names, _ = QFileDialog.getOpenFileNames(self, "Open Data Files", "", "CSV Files
(*.csv)")
if file_names:
try:
self.data = pd.concat([pd.read_csv(file) for file in file_names], ignore_index=True)
self.data['Index'] = self.data.index # Using index for sorting instead of date
self.label.setText("Data loaded.")
self.calculate_total_consumption() # Calculate total consumption upon loading
self.train_model() # Start training automatically
except Exception as e:
self.label.setText("Error loading data: {}".format(str(e)))
else:
self.label.setText("No files selected.")
def train_model(self):
if self.data is None:
self.label.setText("Please load data first.")
return
x = self.data[['energy_consumption']]
45
y = self.data["energy_consumption"]
self.model = RandomForestRegressor(n_estimators=100, random_state=42)
self.model.fit(x, y)
self.label.setText("Model trained.")
def predict(self):
if self.model is None:
self.label.setText("Please train the model first.")
return
days, ok = QInputDialog.getInt(self, "Prediction", "Enter number of days for
prediction:", 60, 1, 365)
if ok:
last_index = self.data.iloc[-1]['Index']
predicted_index = np.arange(last_index + 1, last_index + days + 1).reshape(-1, 1)
x_pred = pd.DataFrame(predicted_index, columns=['energy_consumption'])
predictions = self.model.predict(x_pred)
total_predicted_consumption = predictions.sum()
self.label.setText("Total energy consumption prediction for next {} days:
{:.2f}".format(days, total_predicted_consumption))
self.plot_predictions(predictions, days)
def plot_predictions(self, predictions, days):
plt.figure(figsize=(10, 6))
plt.plot(np.arange(days), predictions, marker='o', linestyle='-')
plt.title("Energy Consumption Prediction for Next {} Days".format(days))
46
plt.xlabel("Day")
plt.ylabel("Consumption")
plt.grid(True)
plt.tight_layout()
plt.show()
def calculate_total_consumption(self):
if self.data is None:
self.label.setText("Please load data first.")
return
total_consumption = self.data['energy_consumption'].sum()
self.label.setText("Total energy consumption: {:.2f}".format(total_consumption))
# Motor ve kullanım alışkanlıkları listesi
motor = {
"tavsiyeler": [
"Motorunuzun üzerindeki yükü azaltmak, enerji tüketimini önemli ölçüde azaltabilir.
Bunu, daha küçük bir motor kullanarak veya motorun yaptığı işi optimize ederek
yapabilirsiniz.",
"Motorun hızını düşürmek de enerji tasarrufu sağlayabilir. Bunu, bir frekans sürücü veya
dişli kutusu kullanarak yapabilirsiniz.",
"Motorunuzu düzenli olarak yağlayın ve onarım ihtiyacı olup olmadığını kontrol edin.
Kirli veya hasarlı bir motor daha fazla enerji tüketecektir.",
"Kayışlar çok gevşek veya çok gerginse enerji kaybına neden olabilir. Kayış gerginliğini
üreticinin önerdiği seviyede tutun.",
"Motorunuzun soğutma sistemi düzgün çalışmalıdır. Yetersiz soğutma, motorun aşırı
ısınmasına ve daha fazla enerji tüketmesine neden olabilir.",
"Motoru aşırı sıcak veya soğuk ortamlarda çalıştırmaktan kaçının. Bu, motorun
verimliliğini düşürebilir ve enerji tüketimini artırabilir.",
"Mümkünse, motorunuzu çalıştırmak için güneş enerjisi veya rüzgar enerjisi gibi
yenilenebilir enerji kaynaklarını kullanın.",
47
"Motorunuz frenleme yaparken enerji üretebiliyorsa, bu enerjiyi depolamak ve daha
sonra kullanmak için bir enerji geri kazanım sistemi kurun."
]
}
# Cihaz seçimini alma (Sabit olarak Motor)
cihaz_secimi = "Motor"
# Kullanıcıya özel tavsiyeler sunma
tavsiyeler = motor["tavsiyeler"]
seçilen_tavsiyeler = random.sample(tavsiyeler, 8)
print(f"{cihaz_secimi} için enerji tasarrufu ipuçları:")
for tavsiye in seçilen_tavsiyeler:
print(f"- {tavsiye}")
if __name__ == "__main__":
app = QApplication(sys.argv)
window = EnergyConsumptionPredictor()
window.show()
sys.exit(app.exec())
