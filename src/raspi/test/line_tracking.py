import cv2
import numpy as np
import time

def gray_detect(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    #灰色のHSVの値域1
    hsv_min = np.array([0,0,60])
    hsv_max = np.array([255,255,120])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    hsv_min = np.array([0,0,60])
    hsv_max = np.array([255,255,120])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask1 + mask2

def line_tracking(img,gray_img):
    gray_pic = cv2.Canny(gray_img,100,200)
    lines = cv2.HoughLinesP(gray_pic,rho=1, theta=np.pi/180,threshold=80, minLineLength=20, maxLineGap=25)
    if type(lines):
        for line in lines:
            x1,y1,x2,y2=line[0]
            hough = cv2.line(img,(x1,y1),(x2,y2),(0,255,0),3)
        return hough
    return img

def blue_detect(img):
     # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hsv_min = np.array([90,64,0])
    hsv_max = np.array([150,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask1
def orange_detect(img):
     # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hsv_min = np.array([9,64,0])
    hsv_max = np.array([29,255,255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)
    return mask1

def analysis_blob(binary_img):
    #connectedComponentsWithStatsmはオブジェクト（連結領域）を検出するメソッド
    labels = cv2.connectedComponentsWithStats(binary_img)

    #ラベルの数（背景もラベリングされるので、オブジェクトの数はlabel[0]-1となる
    n_labels = labels[0]-1

    #起動時やオブジェクトが完全にない場合に、背景しか抽出されない場合がある
    if n_labels == 0:
        return 0

    #背景は0とラベリングされるので、最初の行を削除して格納する
    #dataにはそのラベルの {左上のx座標、左上のy座標、幅、高さ、面積}の情報が格納されている
    data = np.delete(labels[2], 0, axis=0)

    #オブジェクトの重心
    #center = np.delete(labels[3], 0, axis=0)
    #面積が最大値のラベルのインデックス
    max_index = np.argmax(data[:, 4])
    #一番大きいオブジェクトの情報を抽出
    maxblob = {}
    #maxblob["upper_left"] = (data[:, 0][max_index], data[:, 1][max_index]) # 左上座標
    maxblob["width"] = data[:, 2][max_index]  # 幅
    maxblob["height"] = data[:, 3][max_index]  # 高さ
    maxblob["area"] = data[:, 4][max_index]   # 面積（1280×720のうちのピクセル数、環境によって違うかも）
    #maxblob["center"] = center[max_index]  # 中心座標
    area = data[:, 4][max_index]
    #print(area)

    return maxblob

def curveLine_tracking(img):
    blue = blue_detect(img)
    orange = orange_detect(img)

    blue_info = analysis_blob(blue)
    orange_info = analysis_blob(orange)

    #線だと判定する面積の閾値
    threshold = 100

    if blue_info['area'] < threshold and orange_info['area'] < threshold :
        return None,blue,orange
    elif blue_info['area'] >= orange_info['area']:
        return 'blue',blue,orange
    else :
        return 'orange',blue,orange

    

if __name__ == '__main__':
    direction = ""
    cap = cv2.VideoCapture(0)
    imgl = cv2.imread("pic5.png")

    gray = gray_detect(imgl)

    hough = line_tracking(imgl,gray)

    img = cv2.imread("pic6.png")
    line_color, blue, orange = curveLine_tracking(img)
    if line_color == 'blue':
        direction = 'left'
        print('blue')
    elif line_color == 'orange':
        print("orange")
        direction = 'right'
    else :
        print("none")

    cv2.imshow("imgl",imgl)
    cv2.imshow("gray",gray)
    cv2.imshow("img",img)
    cv2.imshow("orange",orange)
    cv2.imshow("blue",blue)
    cv2.waitKey(20000)

    cap.release()
    cv2.destroyAllWindows()
