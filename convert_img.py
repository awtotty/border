import cv2 

gray = cv2.imread("border_imgs/litho/WalkersStudyLitho.jpg", cv2.IMREAD_GRAYSCALE)
backtorgb = cv2.cvtColor(gray,cv2.COLOR_GRAY2RGB)
cv2.imwrite("border_imgs/litho/WalkersStudyLitho_color.jpg", backtorgb)