#camera capture module

#terminal commands
#>>>sudoraspi-config
#>interfacing opt
#>camera
#>enable and reboot

import aws_s3
from datetime import datetime
from picamera import PiCamera


class Camera:
    def Capture(self,camera_object,x_axis=0,y_axis=0):
        _camera = camera_object
        date_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name = str(x_axis)+'_'+str(y_axis)+'_'+date_time+'.jpg'
        _camera.capture(file_name)
        # aws_s3_upload.upload_file(file_name)
        _s3_obj = aws_s3.Aws_S3()
        _s3_obj.upload_file(file_name)
       # del _camera
       # del _s3_obj

if __name__ == "__main__":
    cam_obj = Camera()
    camera_object = PiCamera()
    cam_obj.Capture(camera_object)
    cam_obj.Capture(camera_object,1,1)
