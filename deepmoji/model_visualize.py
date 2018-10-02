from keras.utils.vis_utils import plot_model
from model_def import deepmoji_architecture

model = deepmoji_architecture(nb_classes=63, nb_tokens=1000, maxlen=100)

plot_model(model, to_file='model_architecture.png', show_shapes=True, show_layer_names=True)
