import nivision as nv

cams = nv.IMAQdxEnumerateCameras(True)

imaqdx = nv.IMAQdxOpenCamera(cams[0].InterfaceName, nv.IMAQdxCameraControlModeController)

