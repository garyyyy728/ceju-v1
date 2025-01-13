import numpy as np
import pyrealsense2 as rs
import cv2
import time


####################仅仅是一个示例###################################


# 双目相机参数

class stereoCamera(object):
    def __init__(self):
        try:
            # 创建RealSense管线
            self.pipeline = rs.pipeline()
            self.config = rs.config()
            
            # 查找连接的设备
            ctx = rs.context()
            devices = ctx.query_devices()
            if len(devices) == 0:
                raise Exception("未找到RealSense设备")
            
            # 获取设备序列号
            device = devices[0]
            serial_number = device.get_info(rs.camera_info.serial_number)
            
            # 重置设备
            device.hardware_reset()
            time.sleep(2)  # 等待设备重置
            
            # 配置双目流
            self.config.enable_device(serial_number)
            
            # 使用最低的分辨率和帧率
            self.config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 6)
            self.config.enable_stream(rs.stream.infrared, 2, 640, 480, rs.format.y8, 6)
            
            # 开启流之前先停止所有正在运行的流
            try:
                self.pipeline.stop()
            except:
                pass
            
            # 开启流
            self.profile = self.pipeline.start(self.config)
            
            # 获取深度传感器并设置选项
            depth_sensor = self.profile.get_device().first_depth_sensor()
            if depth_sensor:
                # 设置激光发射器的功率
                if depth_sensor.supports(rs.option.laser_power):
                    depth_sensor.set_option(rs.option.laser_power, 0)  # 关闭激光发射器
                    
                # 设置自动曝光
                if depth_sensor.supports(rs.option.enable_auto_exposure):
                    depth_sensor.set_option(rs.option.enable_auto_exposure, 1)
            
            # 等待设备预热
            time.sleep(3)
            
            # 丢弃前几帧，但设置较短的超时时间
            for _ in range(10):
                try:
                    self.pipeline.wait_for_frames(timeout_ms=100)
                except:
                    continue
            
            # 获取左右红外相机的profile
            left_stream = self.profile.get_stream(rs.stream.infrared, 1)
            right_stream = self.profile.get_stream(rs.stream.infrared, 2)
            
            # 获取内参
            left_intr = left_stream.as_video_stream_profile().get_intrinsics()
            right_intr = right_stream.as_video_stream_profile().get_intrinsics()
            
            # 左相机内参
            self.cam_matrix_left = np.array([[left_intr.fx, 0, left_intr.ppx],
                                            [0, left_intr.fy, left_intr.ppy],
                                            [0, 0, 1]])
            
            # 右相机内参
            self.cam_matrix_right = np.array([[right_intr.fx, 0, right_intr.ppx],
                                             [0, right_intr.fy, right_intr.ppy],
                                             [0, 0, 1]])
            
            # 左右相机畸变系数:[k1, k2, p1, p2, k3]
            self.distortion_l = np.array([[left_intr.coeffs[0], 
                                         left_intr.coeffs[1],
                                         left_intr.coeffs[2],
                                         left_intr.coeffs[3],
                                         left_intr.coeffs[4]]])
            
            self.distortion_r = np.array([[right_intr.coeffs[0],
                                         right_intr.coeffs[1],
                                         right_intr.coeffs[2],
                                         right_intr.coeffs[3],
                                         right_intr.coeffs[4]]])
            
            # 获取外参
            extr = left_stream.get_extrinsics_to(right_stream)
            
            # 旋转矩阵
            self.R = np.array(extr.rotation).reshape(3,3)
            
            # 平移向量
            self.T = np.array(extr.translation).reshape(3,1)  # 转换为列向量
            
            # 焦距
            self.focal_length = left_intr.fx
            
            # 基线距离
            self.baseline = abs(extr.translation[0]) # 单位:米
            
            # 计算Q矩阵
            R1, R2, P1, P2, self.Q, roi1, roi2 = cv2.stereoRectify(
                self.cam_matrix_left, self.distortion_l,
                self.cam_matrix_right, self.distortion_r,
                (640, 480), self.R, self.T, alpha=0)
            
        except Exception as e:
            print(f"相机初始化错误: {str(e)}")
            raise

    def __del__(self):
        try:
            self.pipeline.stop()
        except:
            pass

        


