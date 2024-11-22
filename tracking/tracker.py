from deep_sort_realtime.deepsort_tracker import DeepSort

class Tracker:
    def __init__(self, max_age=30, n_init=3, nn_budget=20):
        self.tracker = DeepSort(max_age=max_age, n_init=n_init, nn_budget=nn_budget)

    def update(self, detections, frame):
        """
        Обновляет трекинг на основе детекций.
        Возвращает список треков: [{'track_id': ID, 'bbox': (x1, y1, x2, y2)}, ...]
        """
        formatted_detections = [((x1, y1, x2, y2), conf, "person") for x1, y1, x2, y2, conf in detections]
        tracks = self.tracker.update_tracks(formatted_detections, frame=frame)

        active_tracks = []
        for track in tracks:
            if not track.is_confirmed():
                continue
            x1, y1, x2, y2 = track.to_ltwh()
            active_tracks.append({
                'track_id': track.track_id,
                'bbox': (x1, y1, x2, y2)
            })
        return active_tracks
