from utility import*
    
def get_headpose(path, model, doPlot = False):
    image = cv2.imread(path)
    rgb = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB)
    x, y, w, h = 25, 100, 775, 900
    cropped = rgb[y:y+h, x:x+w]
    if doPlot:
        pitch, yaw, roll = model.predict(cropped)
        model.draw_axis(cropped, yaw, pitch, roll)
        return cropped
    else:      
        pitch, yaw, roll = model.predict(cropped)
        return pitch[0], yaw[0], roll[0]
    

def get_eyes(image_path, predictor, face_detector, eye_region_scale=1.1, doPlot=False):
    image = cv2.imread(image_path)
    x, y, w, h = 25, 100, 700, 700
    image_cropped = image[y:y+h, x:x+w]
    image_cropped_gray = cv2.cvtColor(image_cropped, cv2.COLOR_BGR2GRAY)
    faces = face_detector(image_cropped_gray, upsample_num_times=0)
    if len(faces) != 1:
        result = None
        return result
    shape = predictor(image_cropped_gray, faces[0])
    landmarks = [(shape.part(i).x + x, shape.part(i).y + y) for i in range(shape.num_parts)]
    left_eye_landmarks = landmarks[36:42]
    right_eye_landmarks = landmarks[42:48]
    left_eye_pts = np.array(left_eye_landmarks, dtype=int)
    eye_region_size = int(np.linalg.norm(left_eye_pts[0] - left_eye_pts[3]) * eye_region_scale)
    left_eye_cropped = image[max(0, left_eye_pts[0][1] - eye_region_size//2):min(image.shape[0], left_eye_pts[3][1] + eye_region_size//2),
                             max(0, left_eye_pts[0][0] - eye_region_size//2):min(image.shape[1], left_eye_pts[2][0] + eye_region_size//2)]
    if left_eye_cropped.size == 0:
        result = None
        return result
    #left_eye_cropped_rgb = cv2.cvtColor(left_eye_cropped, cv2.COLOR_BGR2RGB) #questo lo faccio dopo
    left_pupil = np.mean(left_eye_landmarks, axis=0, dtype=int)
    right_pupil = np.mean(right_eye_landmarks, axis=0, dtype=int)
    if doPlot:
        image_copy = image.copy()
        image_copy = cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB)
        for (x, y) in landmarks:
            cv2.circle(image_copy, (x, y), 10, (0, 255, 0), -1)
        cv2.circle(image_copy, tuple(left_pupil), 10, (255, 0, 0), -1)
        cv2.circle(image_copy, tuple(right_pupil), 10, (255, 0, 0), -1)
        result = [left_eye_cropped, image_copy]
        return result
    result = [left_eye_cropped, left_pupil, right_pupil]
    return result


