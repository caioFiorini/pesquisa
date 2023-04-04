import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Classifier

jvm.start()
help(jvm.start)

l = Loader("weka.core.converters.ArffLoader")
data = l.load_file("iris.arff")

data.class_index = data.num_attributes - 1

cls = Classifier(classname="weka.classifiers.trees.J48", options=["-C", "0.3"])
cls.build_classifier(data)

for index, inst in enumerate(data):
    pred = cls.classify_instance(inst)
    dist = cls.distribution_for_instance(inst)
    print(str(index+1) + ": label index=" + str(pred) + ", class distribution=" + str(dist))

