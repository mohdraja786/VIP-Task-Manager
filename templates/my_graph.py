import matplotlib.pyplot as plt

# 1. डेटा तैयार किया
days = [1, 2, 3, 4, 5]
temperature = [30, 32, 35, 28, 31]

# 2. ग्राफ बनाया (X-axis पर दिन, Y-axis पर तापमान)
plt.plot(days, temperature)

# 3. ग्राफ को नाम दिए ताकि समझ आए कि यह क्या है
plt.xlabel("Days (दिन)")
plt.ylabel("Temperature (तापमान)")
plt.title("5 Days Temperature Report")

# 4. ग्राफ को स्क्रीन पर दिखाया
plt.show()