#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019 Evan Gaustad
#
# This file is part of packer-triage.
#
# packer-triage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# packer-triage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with packer-triage.  If not, see <https://www.gnu.org/licenses/>.

import pandas as pd
import seaborn as sns
import matplotlib.ticker as ticker

def get_plot(file1, file2, label1, label2, title, save_plot_filename):
    df_train_acc = pd.read_csv(file1)[['Value']]
    df_validation_acc = pd.read_csv(file2)[['Value']]
    df_train_acc = df_train_acc.rename(columns={"Value": label1})
    df_validation_acc = df_validation_acc.rename(columns={"Value": label2})
    accuracy = df_validation_acc.join(df_train_acc)
    sns_plot = sns.lineplot(hue='variable', data=accuracy, size=505)
    sns_plot.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    sns_plot.set_title(title)
    sns_plot.set_ylabel('Accuracy')
    sns_plot.set_xlabel('Epoch')
    sns_plot.figure.savefig(save_plot_filename)
    return sns_plot

if(__name__ == '__main__'):
    # plots generated from exported data from tensorboard
    file1 = './run-PackerIdentifier-medium-20_epochs_2019-07-22T080440.312456_train-tag-epoch_accuracy.csv'
    file2 = './run-PackerIdentifier-medium-20_epochs_2019-07-22T080440.312456_validation-tag-epoch_accuracy.csv'
    label1 = "train_accuracy"
    label2 = "validation_accuracy"
    title = 'Accuracy During Training'
    save_plot_filename = './accuracy_plot.png'
    get_plot(file1, file2, label1, label2, title, save_plot_filename)

    file1 = './run-PackerIdentifier-medium-20_epochs_2019-07-22T080440.312456_train-tag-epoch_loss.csv'
    file2 = './run-PackerIdentifier-medium-20_epochs_2019-07-22T080440.312456_validation-tag-epoch_loss.csv'
    label1 = "train_loss"
    label2 = "validation_loss"
    title = 'Loss During Training'
    save_plot_filename = './loss_plot.png'
    get_plot(file1, file2, label1, label2, title, save_plot_filename)

