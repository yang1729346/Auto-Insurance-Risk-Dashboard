---
Ext:
    - .csv

DatasetUsage:
    - 43107050

FolderName:
    - /home/mw/input/qcbx8323/
---

## **背景描述**
汽车保险公司针对投保车辆出事故的索赔预测决定了投保车辆的投保成本。索赔预测结果不准确的话，一方面会提高索赔风险较低的司机的保险价格，导致失去客户；另一方面会降低存在问题司机的保险价格，造成严重的损失。

## **数据说明**
policy_id	投保人的唯一标识符
policy_tenure	投保的时间段
age_of_car	汽车年龄（归一化）
age_of_policyholder	投保人年龄（归一化）
area_cluster	投保人的区域集群
population_density	投保人所属城市人口密度
make	汽车所属制造商/公司
segment	汽车部分（A/B1/B2/C1/C2）
model	编码的汽车名称
fuel_type	汽车使用的燃料类型
max_torque	汽车产生的最大扭矩
max_power	汽车产生的最大功率
engine_type	汽车中使用的发动机类型
airbags	车内安装的安全气囊数量
is_esc	汽车中是否存在电子稳定控制
is_adjustable_steering	汽车的方向盘是否可调
is_tpms	轮胎压力监测系统是否存在于汽车中
is_parking_sensors	汽车中是否存在停车传感器
is_parking_camera	停车摄像头是否在车内
rear_brakes_type	汽车后部使用的制动器类型
displacement	汽车的发动机排量
cylinder	汽车发动机中的气缸数
transmission_type	汽车的变速箱类型
gear_box	车里的齿轮数
steering_type	汽车中存在的动力转向类型
turning_radius	车辆进行一定转弯所需的空间（米）
length	汽车长度（毫米）
width	汽车宽度（毫米）
height	汽车高度（毫米）
gross_weight	满载汽车的最大允许重量，包括乘客、货物和设备（公斤）
is_front_fog_lights	汽车内是否有前雾灯
is_rear_window_wiper	后窗雨刷器在汽车中是否可用
is_rear_window_washer	后窗垫圈在汽车中是否可用
is_rear_window_defogger	车内后窗除雾器是否可用
is_brake_assist	制动辅助功能在汽车中是否可用
is_power_door_locks	汽车中是否有电动门锁
is_central_locking	中央锁定功能是否在汽车中可用
is_power_steering	汽车中是否有动力转向
is_driver_seat_height_adjustable	驾驶座的高度是否可调
is_day_night_rear_view_mirror	汽车中是否存在日夜后视镜
is_ecw	发动机检查警告（ECW）在汽车中是否可用
is_speed_alert	速度警报系统在汽车中是否可用
ncap_rating	NCAP给出的安全等级（5分）
target	投保人是否在未来6个月内提出索赔


## **数据来源**
科大讯飞挑战赛

## **问题描述**
根据投保人基本信息和汽车相关信息，数据集包含有关具有保单保有权、汽车年龄、车主年龄、城市人口密度、汽车制造商和型号、动力、发动机类型等属性的投保人的信息，预测投保人是否在未来6个月内提出索赔的目标变量。

## **引用格式**
```
@misc{qcbx8323,
    title = { 汽车保险索赔数据集 },
    author = { 小虎鲸5ieu },
    howpublished = { \url{https://www.heywhale.com/mw/dataset/6509214f3620e3431115b917} },
    year = { 2023 },
}
```