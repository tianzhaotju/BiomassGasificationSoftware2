from .Blur import Blur
from .Cost import Cost
import math
class InputParam():
	def __init__(self):
		#用户输入
		self.table_burden = [
							[0, 50],
							[6, 70],
							[12, 90],
							[18, 130],
							[24, 170],
							[30, 190],
							[36, 230],
							[42, 210],
							[48, 180],
							[54, 150],
							[60, 170],
							[66, 190],
							[72, 180],
							[78, 160],
							]
		self.range_intake_air = [9.5, 16.5]
		self.range_intake_material = [0, 100]
		self.range_derta_intake_air = [0, 5]
		self.range_derta_intake_material = [0, 20]
		self.weights_perform = [0.33, 0.33, 0.33]
		self.weights_air_material = [0.7, 0.3]
		self.CHSON = [46.2, 5.1, 0.06, 35.4, 1.5]

		#内部变量
		#模糊控制的开始时间
		self.start_time = 0
		#模糊控制的时间段，单位min
		self.time_length_blur = 60
		self.blur = Blur()
		self.cost = Cost()
		#标准化区间
		self.standard_burden = [0, 300]
		self.standard_intake_air = [9.5, 16.5]
		self.standard_intake_material = [0, 100]
		self.standard_Tg = [360, 850]
		self.standard_H2 = [4, 12]
		self.standard_CH4 = [1, 4]
		self.standard_CO = [10, 28]
		self.standard_CO2 = [5, 25]
		self.standard_CQL = [0.5, 3]
		self.standard_QHXL = [0.1, 0.9]
		self.standard_CQRZ = [3,5, 7]



	#获得进气量范围[9.5, 16.5]
	def get_range_intake_air(self):
		return self.range_intake_air

	#获得进料量范围[0, 100]
	def get_range_intake_material(self):
		return self.range_intake_material

	#获得进气量变化范围[0, 5]
	def get_range_derta_intake_air(self):
		return self.range_derta_intake_air

	#获得进料量变化范围[0, 20]
	def get_range_derta_intake_material(self):
		return self.range_derta_intake_material

	#设置开始时间
	def set_start_time(self, settime):
		self.start_time = settime
		return True

	#获得用于模糊控制的Yref和P,
	def __get_dertaY_P(self):
		present_burdens = []
		lborder_time = self.start_time
		rborder_time = self.start_time + self.time_length_blur
		for burden in self.table_burden:
			if lborder_time <= burden[0] and burden[0] <= rborder_time:
				present_burdens.append(burden)

		maxY = 0
		minY = 1000
		P = 0
		for i in range(len(present_burdens)):
			if present_burdens[i][1] < minY:
				minY = present_burdens[i][1]
			if present_burdens[i][1] > maxY:
				maxY = present_burdens[i][1]
			if i != 0 and i != len(present_burdens) - 1:
				lburden = present_burdens[i-1][1]
				mburden = present_burdens[i][1]
				rburden = present_burdens[i+1][1]
				#极大
				if mburden > lburden and mburden > rburden:
					P = P+1
				#极小
				if mburden < lburden and mburden < rburden:
					P = P+1

		Y = maxY - minY
		#Y = 180
		#P = 2
		#print("△Y: ", Y)
		#print("P: ", P)
		return Y, P

	#预测时域Hp、跟踪误差成本权重Q
	def __get_Hp_Q(self):
		Y, P = self.__get_dertaY_P()
		return self.blur.get_Hp_Q(Y, P)

	#得到控制时域
	def get_control_time(self):
		Hp, Q = self.__get_Hp_Q()
		control_time = Hp
		return control_time

	def __get_demand_burden(self):
		for i in range(len(self.table_burden)):
			if self.table_burden[i][0] == self.start_time:
				return self.table_burden[i][1]
			elif i == len(self.table_burden) - 1:
				return self.table_burden[i][1]
			elif self.table_burden[i][0] < self.start_time and self.start_time < self.table_burden[i+1][0]:
				time1 = self.table_burden[i][0]
				time2 = self.table_burden[i+1][0]
				burden1 = self.table_burden[i][1]
				burden2 = self.table_burden[i+1][1]
				return burden1 + (burden2 - burden1) * (self.start_time - time1) / (time2 - time1)

	def __get_weights(self):
		Hp, Q = self.__get_Hp_Q()
		T = (1-Q) / 2
		weights_Q = [[Q]]
		weights_R = [[self.weights_air_material[0], 0], [0, self.weights_air_material[1]]]
		weights_T = [self.weights_perform]
		return weights_Q, weights_R, weights_T, T

	def __normalized_value(self, value, range):
		return (value - range[0]) / (range[1] - range[0])

	def __normalized_derta(self, derta, range):
		return derta / (range[1] - range[0])

	def get_cost(self, intake_air, intake_material, H2, CH4, CO, Tg, derta_intake_air, derta_intake_material):
		H2 = H2/100.0
		CH4 = CH4/100.0
		CO = CO/100.0
		#CO2=CO/2.18/e^(-450.893/(Tg+273))
		CO2 = CO / 2.18 / math.exp(-450.893/(Tg+273))
		N2 = 1 - CO2 - H2 - CH4 - CO
		CQRZ = 12.6*CO + 10.8*H2 + 35.9*CH4
		CQL = (intake_material + 1.29*intake_air) / (44.6*
		(H2*2 + CH4*16 + CO*28 + CO2*44 + N2*28)/1000) / intake_material
		HHV = 0.3491*self.CHSON[0] + 1.1783*self.CHSON[1] + 0.1005*self.CHSON[2] - 0.1034*self.CHSON[3] - 0.0151*self.CHSON[4]
		YLRZ = HHV - 2.256*9*self.CHSON[1]/100
		QHXL = CQRZ * CQL / YLRZ

		weights_Q, weights_R, weights_T, T = self.__get_weights()
		#print("weights_Q: ", weights_Q)
		#print("weights_R: ", weights_R)
		#print("weights_T: ", weights_T)
		#print("T: ", T)
		product_burden = CQRZ * CQL * intake_material / 3.6
		demand_burden = self.__get_demand_burden()
		#print("生产负荷: ", product_burden)
		#print("需求负荷: ", demand_burden)
		derta_burden = product_burden - demand_burden
		_derta_burden = self.__normalized_derta(derta_burden, self.standard_burden)
		print('burden:\n', derta_burden)
		C1 = self.cost.get_burden_cost([_derta_burden], weights_Q)*100

		derta_intake_air = self.__normalized_derta(derta_intake_air, self.standard_intake_air)
		derta_intake_material = self.__normalized_derta(derta_intake_material, self.standard_intake_material)
		C2 = self.cost.get_control_cost([derta_intake_air, derta_intake_material], weights_R, T)*10

		LHV = CQRZ
		Tg = Tg
		effect = QHXL
		LHV = self.__normalized_value(LHV, self.standard_CQRZ)
		Tg = self.__normalized_value(Tg, self.standard_Tg)
		effect = self.__normalized_value(effect, self.standard_QHXL)
		C3 = self.cost.get_perform_cost(LHV, Tg, effect, weights_T, T)
		#print("H2: ", H2)
		#print("CH4: ", CH4)
		#print("CO: ", CO)
		#print("CO2: ", CO2)
		#print("N2: ", N2)
		#print("原料热值 : ", YLRZ)
		#print("产气热值: ", CQRZ)
		#print("产气率: ", CQL)
		#print("气化效率: ", QHXL)
		#print("跟踪误差成本: ", C1)
		#print("控制量变化幅值成本: ", C2)
		#print("工艺性能成本: ", C3)
		return C1 + C2 + C3























