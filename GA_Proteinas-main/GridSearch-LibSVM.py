#!/usr/bin/python
# -*- coding: utf-8 -*-

import weka.core.jvm as jvm
from weka.core.converters import Loader
from weka.classifiers import Classifier, Evaluation, SingleClassifierEnhancer
import javabridge

jvm.logger.setLevel(jvm.logging.WARNING)
jvm.start(packages=True, max_heap_size="512m")

# Each instance has nominal class and numeric attributes
loader = Loader(classname="weka.core.converters.ArffLoader")
trainData = loader.load_file('iris.arff')
trainData.class_is_last()

# LibSVM with RBF kernel, cost C and gamma should be optimized
classifier = Classifier(classname="weka.classifiers.functions.LibSVM",\
                    options=["-S", "0", "-K", "2", "-Z", "-G", "0.0", "-C", "1.0",
                             "-D", "3", "-R", "0.0", "-N", "0.5", "-M", "40.0",
                             "-E", "0.001", "-P", "0.1", "-model", "/home/sebastian", "-seed", "1"])

# Logaritmic grid search on C and gamma, with cross validation (mandatory) on the training set
grid = SingleClassifierEnhancer(
    classname="weka.classifiers.meta.GridSearch",
    options=[
        "-E", "ACC",
        "-x-property", "cost", "-x-min", "-3.0", "-x-max", "3.0", "-x-step", "1.0", "-x-base", "10.0",
        "-x-expression", "pow(BASE,I)",
        "-y-property", "gamma", "-y-min", "-3.0", "-y-max", "3.0", "-y-step", "1.0", "-y-base", "10.0",
        "-y-expression", "pow(BASE,I)",
        "-output-debug-info",
        "-W", "weka.classifiers.trees.J48",  # dummy classifier added to avoid Nominal Class Capability Exception
        "-sample-size", "100.0", "-num-slots", "1", "-S", "1"])

# LibSVM is added to grid configuration
grid.classifier = classifier
# Search for the best parameters and build a classifier with them
grid.build_classifier(trainData)
best = Classifier(jobject=javabridge.call(grid.jobject, "getBestClassifier", "()Lweka/classifiers/Classifier;"))
best.build_classifier(trainData)

print grid
print best

# Evaluation on train dataset just to simplify this example
evaluation = Evaluation(trainData)
evaluation.test_model(best, trainData)
print best.to_commandline()
print evaluation.matrix()

jvm.stop()
