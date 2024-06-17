import numpy as np
from numpy import linalg as LA

class SingleCamera:

    def __init__(self, global_cd, pixel_cd, n):

        self.__global_cd = global_cd
        self.__pixel_cd = pixel_cd
        self.__point_num = n

        '''
            0. P是Pm=0时的适当形式
            1. svd解出的M是已知的，这意味着相机矩阵的真实值是M的标量倍，记录为__roM
            2. M可以表示为形式[A b]，其中A是3x3矩阵，b的形状为3x1
            3. K是本征相机矩阵
            4. R和t用于旋转和平移

        '''
        self.__P = np.empty([self.__point_num, 12], dtype=float)
        self.__roM = np.empty([3, 4], dtype=float)
        self.__A = np.empty([3, 3], dtype=float)
        self.__b = np.empty([3, 1], dtype=float)
        self.__K = np.empty([3, 3], dtype=float)
        self.__R = np.empty([3, 3], dtype=float)
        self.__t = np.empty([3, 1], dtype=float)

    def returnAb(self):
        return self.__A, self.__b

    def returnKRT(self):
        return self.__K, self.__R, self.__t

    def returnM(self):
        return self.__roM

    def myReadFile(filePath):
        pass

    def changeHomo(no_homo):
        pass

    # to compose P in right form s.t. we can get Pm=0
    def comP(self):
        i = 0
        P = np.empty([self.__point_num, 12], dtype=float)
        # print(P.shape)
        while i < self.__point_num:
            c = i // 2
            p1 = self.__global_cd[c]
            p2 = np.array([0, 0, 0, 0])
            if i % 2 == 0:
                p3 = -p1 * self.__pixel_cd[c][0]
                # print(p3)
                P[i] = np.hstack((p1, p2, p3))

            elif i % 2 == 1:
                p3 = -p1 * self.__pixel_cd[c][1]
                # print(p3)
                P[i] = np.hstack((p2, p1, p3))
            # M = P[i]
            # print(M)
            i = i + 1
        print("Now P is with form of :")
        print(P)
        print('\n')
        self.__P = P

    # svd to P，return A,b, where M=[A b]
    def svP(self):
        U, sigma, VT = LA.svd(self.__P)
        # print(VT.shape)
        V = np.transpose(VT)
        preM = V[:, -1]
        roM = preM.reshape(3, 4)
        print("some scalar multiple of M,recorded as roM:")
        print(format(roM))
        print('\n')
        A = roM[0:3, 0:3].copy()
        b = roM[0:3, 3:4].copy()
        print("M can be written in form of [A b], where A is 3x3 and b is 3x1, as following:")
        print(A)
        print(b)
        print('\n')
        self.__roM = roM
        self.__A = A
        self.__b = b

    # solve the intrinsics and extrisics
    def work(self):
        # compute ro, where ro=1/|a3|, ro may be positive or negative,
        # we choose the positive ro and name it ro01
        a3T = self.__A[2]
        # print(a3T)
        under = LA.norm(a3T)
        # print(under)
        ro01 = 1 / under
        print("The ro is %f \n" % ro01)

        # comput cx and cy
        a1T = self.__A[0]
        a2T = self.__A[1]
        cx = ro01 * ro01 * (np.dot(a1T, a3T))
        cy = ro01 * ro01 * (np.dot(a2T, a3T))
        print("cx=%f,cy=%f \n" % (cx, cy))

        # compute theta
        a_cross13 = np.cross(a1T, a3T)
        a_cross23 = np.cross(a2T, a3T)
        theta = np.arccos((-1) * np.dot(a_cross13, a_cross23) / (LA.norm(a_cross13) * LA.norm(a_cross23)))
        print("theta is: %f \n" % theta)

        # compute alpha and beta
        alpha = ro01 * ro01 * LA.norm(a_cross13) * np.sin(theta)
        beta = ro01 * ro01 * LA.norm(a_cross23) * np.sin(theta)
        print("alpha:%f, beta:%f \n" % (alpha ,beta))

        # compute K
        K = np.array([alpha, -alpha * (1 / np.tan(theta)), cx, 0, beta / (np.sin(theta)), cy, 0, 0, 1])
        K = K.reshape(3, 3)
        print("We can get K accordingly: ")
        print(format(K))
        print('\n')
        self.__K = K

        # compute R
        r1 = a_cross23 / LA.norm(a_cross23)
        r301 = ro01 * a3T
        r2 = np.cross(r301, r1)
        # print(r1, r2, r301)
        R = np.hstack((r1, r2, r301))
        R = R.reshape(3 ,3)
        print("we can get R:")
        print(format(R))
        print('\n')
        self.__R = R

        # compute T
        T = ro01 * np.dot(LA.inv(K), self.__b)
        print("we can get t:")
        print(format(T))
        print('\n')
        self.__t = T

    def check(self, g_check, p_check):
        my_size = p_check.shape[0]
        my_err = np.empty([my_size])
        for i in range(my_size) :
            test_pix = np.dot(self.__roM, g_check[i])
            u = test_pix[0] / test_pix[2]
            v = test_pix[1] / test_pix[2]
            u_c = p_check[i][0]
            v_c = p_check[i][1]
            print("you get test point %d with result (%f,%f)" % (i, u, v))
            print("the correct result is (%f,%f)" % (u_c ,v_c))
            my_err[i] = (abs( u -u_c ) /u_c +abs( v -v_c ) /v_c ) /2
        average_err = my_err.sum( ) /my_size
        print("The average error is %f ," % average_err)
        if average_err > 0.1:
            print("which is more than 0.1")
        else:
            print("which is smaller than 0.1, the M is acceptable")

# The homogeneous world coodinate

# Although it would be more appropriate to write a function to read the coordinates,
# we've simplified it by listing the coordinates directly in array.

# world corrdinate
# points: (8, 0, 9), (8, 0, 1), (6, 0, 1), (6, 0, 9)
g_xz = np.array([8, 0, 9, 1, 8, 0, 1, 1, 6, 0, 1, 1, 6, 0, 9, 1])
g_xz = g_xz.reshape(4, 4)
# points: (5, 1, 0), (5, 9, 0), (4, 9, 0), (4, 1, 0)
g_xy = np.array([5, 1, 0, 1, 5, 9, 0, 1, 4, 9, 0, 1, 4, 1, 0, 1])
g_xy = g_xy.reshape(4, 4)
# points: (0, 4, 7), (0, 4, 3), (0, 8, 3), (0, 8, 7)
g_yz = np.array([0, 4, 7, 1, 0, 4, 3, 1, 0, 8, 3, 1, 0, 8, 7, 1])
g_yz = g_yz.reshape(4, 4)
g_coor = np.vstack((g_xz, g_xy, g_yz))
#print(g_coor)
# pixel coordinate
p_xz = np.array([275, 142, 312, 454, 382, 436, 357, 134])
p_xz = p_xz.reshape(4, 2)
p_xy = np.array([432, 473, 612, 623, 647, 606, 464, 465])
p_xy = p_xy.reshape(4, 2)
p_yz = np.array([654, 216, 644, 368, 761, 420, 781, 246])
p_yz = p_yz.reshape(4, 2)
p_coor = np.vstack((p_xz, p_xy, p_yz))
#print(c_coor)
# coordinate for validation whether the M is correct or not
g_check = np.array([6, 0, 5, 1, 3, 3, 0, 1, 0, 4, 0, 1, 0, 4, 4, 1, 0, 0, 7, 1])
g_check = g_check.reshape(5, 4)
p_check = np.array([369, 297, 531, 484, 640, 468, 646, 333, 556, 194])
p_check = p_check.reshape(5, 2)


aCamera = SingleCamera(g_coor, p_coor, 12)  # 12 points in total are used
aCamera.comP()
aCamera.svP()
aCamera.work()  # print computed result
aCamera.check(g_check, p_check)  # test 5 points and verify M