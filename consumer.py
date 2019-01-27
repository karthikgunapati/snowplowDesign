from kafka import KafkaConsumer
from snowplow_analytics_sdk.event_transformer import transform
from pydblite.pydblite import Base
import json
from snowplow_analytics_sdk.snowplow_event_transformation_exception import SnowplowEventTransformationException


db = Base('/root/analytics.pydb', save_to_file=True)
if db.exists():
    db.open()
else:
    db.create('user_id', 'action', 'vedio_id', 'viewed_time', 'total_time', 'seeked')

class MyConsumer(object):
    def __init__(self, topic, bootstrap_servers):
        self.consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers,
        api_version=(0,10), auto_offset_reset='earliest', enable_auto_commit=False)
        # value_deserializer= lambda m: json.loads(m))
        # m.decode('ISO-8859-1')
    
    def clean_msg(self, msg):
        try:
            return json.loads(json.dumps(transform(msg.decode())))
        except SnowplowEventTransformationException as e:
            return e.error_messages

    def run(self):
        for msg in self.consumer:
            doc = self.clean_msg(msg.value)
            db.insert(
                seeked=doc['unstruct_event_com_tectoro_viewed-vedio_1']['seeked'],
                user_id=doc['user_id'],
                action=doc['unstruct_event_com_tectoro_viewed-vedio_1']['action'],
                vedio_id=doc['unstruct_event_com_tectoro_viewed-vedio_1']['vedioId'],
                viewed_time=doc['unstruct_event_com_tectoro_viewed-vedio_1']['viewedTime'],
                total_time=doc['unstruct_event_com_tectoro_viewed-vedio_1']['totalTime'],   
            )
            db.commit()
            print ("value=%s\n\n" % doc)


if __name__ == '__main__':
    MyConsumer('good_enrich', ['kafka:9092']).run()
