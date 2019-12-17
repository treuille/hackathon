"""Streamlit UI for the interactive generation of images."""

import streamlit as st
import sys

st.title("Shaobo's TL-GAN Project")

import os
import glob
import numpy as np
import time
import pickle
# import tensorflow as tf
import PIL
import matplotlib
import inspect
matplotlib.use('TkAgg')

sys.path.append('src')
import tl_gan.feature_axis as feature_axis
import tl_gan.load_model as load_model

# import matplotlib.pyplot as plt
# import matplotlib.widgets as widgets
# plt.ion()

def main2():
    def gen_time_str():
        """ tool function """
        return time.strftime("%Y%m%d_%H%M%S", time.gmtime())

    # """ location to save images """
    path_gan_explore_interactive = './asset_results/pggan_celeba_feature_axis_explore_interactive/'
    if not os.path.exists(path_gan_explore_interactive):
        os.mkdir(path_gan_explore_interactive)

    # """ load feature directions """
    path_feature_direction = './asset_results/pg_gan_celeba_feature_direction_40'

    @st.cache
    def load_feature_direction_name(path_feature_direction):
        pathfile_feature_direction = glob.glob(os.path.join(path_feature_direction, 'feature_direction_*.pkl'))[-1]

        with open(pathfile_feature_direction, 'rb') as f:
            feature_direction_name = pickle.load(f)

        return feature_direction_name

    feature_direction_name = load_feature_direction_name(path_feature_direction)
    feature_direction = feature_direction_name['direction']
    feature_name = feature_direction_name['name']
    num_feature = feature_direction.shape[1]


    # st.show(feature_direction)
    # st.show(feature_name)
    # st.show(num_feature)
    # st.show(num_feature)
    # st.write('Here is something...')
    #
    #
    #
    # st.subheader(""" load gan model """)
    #
    #
    # st.subheader(""" create tf session """)
    #
    #
    #
    # st.write('Got to line `%s`.' % inspect.currentframe().f_lineno)
    #
    #
    #
    # st.subheader('load_model()')
    G, D, Gs = load_model.load_gan_model()

    # st.show(G)
    # st.show(D)
    # st.show(Gs)


    num_latent = Gs.input_shapes[0][1]

    # Generate random latent variables
    latents = np.random.randn(1, *Gs.input_shapes[0][1:])
    # Generate dummy labels
    dummies = np.zeros([latents.shape[0]] + Gs.input_shapes[1][1:])

    # st.show(type(Gs))
    # st.write(type(dummies), dummies.shape)
    # st.show(latents.shape[0])
    # st.show(Gs.input_shapes[1][1:])

    def gen_image(latents, dummies):
        """
        tool funciton to generate image from latent variables
        :param latents: latent variables
        :return:
        """
        images = Gs.run(latents, dummies)
        images = np.clip(np.rint((images + 1.0) / 2.0 * 255.0), 0.0, 255.0).astype(np.uint8)  # [-1,1] => [0,255]
        images = images.transpose(0, 2, 3, 1)  # NCHW => NHWC
        return images[0]

    image = st.empty()
    latent_display = st.empty()

    latents = []
    n_sliders = 4
    a = st.slider('a', 500, 0, 1000, 50)
    b = st.slider('b', 500, 0, 1000, 50)
    c = st.slider('c', 500, 0, 1000, 50)
    d = st.slider('d', 500, 0, 1000, 50)
    latents = [a, b, c, d]

    latents = latents * (num_latent // n_sliders)
    latents = np.array(latents, dtype=np.float64).reshape((1, num_latent))
    latents = (latents - 500.0) / 2000.0
    # latent_display.dataframe(latents)

    img_cur = gen_image(latents, dummies)
    image.image(img_cur, use_column_width=True)

    feature_lock_status = np.zeros(num_feature).astype('bool')
    feature_direction_disentangled = \
        feature_axis.disentangle_feature_axis_by_idx(
            feature_direction,
            idx_base=np.flatnonzero(feature_lock_status))
    st.show(feature_lock_status)
    st.show(feature_direction_disentangled)

    st.help(np.max)
    st.show(np.min(np.absolute(feature_direction_disentangled), axis=1))
    st.show(feature_name)

    # # feature_values = []
    # for feature in feature_name:
    #     st.write(feature)

# ##
# """ plot figure with GUI """
# h_fig = plt.figure(figsize=[12, 6])
# h_ax = plt.axes([0.0, 0.0, 0.5, 1.0])
# h_ax.axis('off')
# h_img = plt.imshow(img_cur)
#
# yn_save_fig = True
#
# class GuiCallback(object):
#     counter = 0
#     latents = latents
#     def __init__(self):
#         self.latents = np.random.randn(1, *Gs.input_shapes[0][1:])
#         self.feature_direction = feature_direction
#         self.feature_lock_status = np.zeros(num_feature).astype('bool')
#         self.feature_direction_disentangled = feature_axis.disentangle_feature_axis_by_idx(
#             self.feature_direction, idx_base=np.flatnonzero(self.feature_lock_status))
#         img_cur = gen_image(self.latents)
#         h_img.set_data(img_cur)
#         plt.draw()
#
#     def random_gen(self, event):
#         self.latents = np.random.randn(1, *Gs.input_shapes[0][1:])
#         img_cur = gen_image(self.latents)
#         h_img.set_data(img_cur)
#         plt.draw()
#
#     def modify_along_feature(self, event, idx_feature, step_size=0.05):
#         self.latents += self.feature_direction_disentangled[:, idx_feature] * step_size
#         img_cur = gen_image(self.latents)
#         h_img.set_data(img_cur)
#         plt.draw()
#         plt.savefig(os.path.join(path_gan_explore_interactive,
#                                  '{}_{}_{}.png'.format(gen_time_str(), feature_name[idx_feature], ('pos' if step_size>0 else 'neg'))))
#
#     def set_feature_lock(self, event, idx_feature):
#         self.feature_lock_status[idx_feature] = np.logical_not(self.feature_lock_status[idx_feature])
#         self.feature_direction_disentangled = feature_axis.disentangle_feature_axis_by_idx(
#             self.feature_direction, idx_base=np.flatnonzero(self.feature_lock_status))
#
# callback = GuiCallback()
#
# ax_randgen = plt.axes([0.55, 0.90, 0.15, 0.05])
# b_randgen = widgets.Button(ax_randgen, 'Random Generate')
# b_randgen.on_clicked(callback.random_gen)
#
# def get_loc_control(idx_feature, nrows=8, ncols=5,
#                     xywh_range=(0.51, 0.05, 0.48, 0.8)):
#     r = idx_feature // ncols
#     c = idx_feature % ncols
#     x, y, w, h = xywh_range
#     xywh = x+c*w/ncols, y+(nrows-r-1)*h/nrows, w/ncols, h/nrows
#     return xywh
#
# step_size = 0.4
#
# def create_button(idx_feature):
#     """ function to built button groups for one feature """
#     x, y, w, h = get_loc_control(idx_feature)
#
#     plt.text(x+w/2, y+h/2+0.01, feature_name[idx_feature], horizontalalignment='center',
#              transform=plt.gcf().transFigure)
#
#     ax_neg = plt.axes((x + w / 8, y, w / 4, h / 2))
#     b_neg = widgets.Button(ax_neg, '-', hovercolor='0.1')
#     b_neg.on_clicked(lambda event:
#                      callback.modify_along_feature(event, idx_feature, step_size=-1 * step_size))
#
#     ax_pos = plt.axes((x + w *5/8, y, w / 4, h / 2))
#     b_pos = widgets.Button(ax_pos, '+', hovercolor='0.1')
#     b_pos.on_clicked(lambda event:
#                      callback.modify_along_feature(event, idx_feature, step_size=+1 * step_size))
#
#     ax_lock = plt.axes((x + w * 3/8, y, w / 4, h / 2))
#     b_lock = widgets.CheckButtons(ax_lock, ['L'], [False])
#     b_lock.on_clicked(lambda event:
#                       callback.set_feature_lock(event, idx_feature))
#     return b_neg, b_pos, b_lock
#
# list_buttons = []
# for idx_feature in range(num_feature):
#     list_buttons.append(create_button(idx_feature))
#
# plt.show()
#
#
#
#
# ##
# #sess.close()


with load_model.sess.as_default():
    main2()
