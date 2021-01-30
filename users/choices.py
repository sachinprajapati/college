from datetime import date

BOOLEAN_STATUS = [
	("0", 'Inactive'),
	("1", 'Active')
]

GENDER = [
	("F", 'Female'),
	("M", 'Male')
]

CATEGORY = [
	("G", 'General'),
	("O", 'BC'),
	("E", 'EBC'),
	("C", 'SC'),
	("T", 'ST'),
]

MARITAL_STATUS = [
	("U", 'Unmarried'),
	("M", 'Married'),
	("D", 'Divorce'),
]

RELIGION_LIST = [
	("H", 'Hindu'),
	("M", 'Muslim'),
	("S", 'Sikh'),
	("C", 'Christian'),
	("O", 'Other')
]

DISABLED = [
	("V", 'Visual Impairment'),
	("H", 'Hearing Impairment'),
	("O", 'Ortho Impairment'),
	("N", 'None')
]

STATE = [
	(1, "Andra Pradesh"),
	(2, "Arunachal Pradesh"),
	(3, "Assam"),
	(4, "Bihar"),
	(5, "Chhattisgarh"),
	(6, "Goa"),
	(7, "Gujarat"),
	(8, "Haryana"),
	(9, "Himachal Pradesh"),
	(10, "Jammu and Kashmir"),
	(11, "Jharkhand"),
	(12, "Karnataka"),
	(13, "Kerala"),
	(14, "Madya Pradesh"),
	(15, "Maharashtra"),
	(16, "Manipur"),
	(17, "Meghalaya"),
	(18, "Mizoram"),
	(19, "Nagaland"),
	(20, "Orissa"),
	(21, "Punjab"),
	(22, "Rajasthan"),
	(23, "Sikkim"),
	(24, "Tamil Nadu"),
	(25, "Telagana"),
	(26, "Tripura"),
	(27, "Uttaranchal"),
	(28, "Uttar Pradesh"),
	(29, "West Bengal"),
	(30, "Andaman and Nicobar Islands"),
	(31, "Chandigarh"),
	(32, "Dadar and Nagar Haveli"),
	(33, "Daman and Diu"),
	(34, "Delhi"),
	(35, "Lakshadeep"),
	(36, "Pondicherry")
]

STREAM = [
	('S', 'Science'),
	('C', 'Commerce'),
	('A', 'Arts')
]

MARKS_TYPE = [
	(1, 'Marks'),
	(2, 'CGPA')
]

PREVIOUS_COURSE = [
	# ('10', '10th'),
	# ('12', '12th'),
	('G' , 'Graduation'),
	# ('PG', 'Post Graduation')
]

MERIT_LIST_CHOICES = [
	(1, 'Merit1'),
	(2, 'Merit2'),
	(3, 'Merit3'),
]

FeeHeads = [
	(1, 'Admission'),
	(2, 'First Year'),
	(3, 'Second Year'),
	(4, 'Third Year'),
	(5, 'clc'),
]

DIVISION_LIST = [
	(1, 'First'),
	(2, 'Second'),
	(3, 'Third'),
]

MONTH_LIST = [(i, date(1900, i, 1).strftime('%B')) for i in range(1,13)]

PAYMENT_STATUS = [
	(0, 'failure'),
	(1, 'success')
]

CLC_FEE_TYPE = [
	(1, 'Normal Fee'),
	(2, 'Tatkal Fee'),
]

COURSE_TYPE = [
	(1, 'Vocational UG'),
	(2, 'Vocational PG'),
	(3, 'General PG'),
]