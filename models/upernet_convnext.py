# Copyright (c) Meta Platforms, Inc. and affiliates.

# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
import torch
import torch.nn as nn
from backbone.convnext import ConvNeXt
from decoder.uperhead import UPerHead


class upernet_convnext(nn.Module):
    def __init__(self, in_chans, out_chans):
        super().__init__()
        self.backbone = ConvNeXt(in_chans=in_chans)
        self.decoder = UPerHead(in_channels=[16, 32, 64, 128],  # tiny的参数
                                in_index=[0, 1, 2, 3],
                                pool_scales=(1, 2, 3, 6),
                                channels=out_chans,
                                dropout_ratio=0.1,
                                num_classes=out_chans,
                                norm_cfg=dict(type='BN', requires_grad=True),
                                align_corners=False,
                                loss_decode=dict(
                                    type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0))

    def forward(self, x):
        backbone_out = self.backbone(x)
        out = self.decoder(backbone_out)
        return out


# norm_cfg = dict(type='SyncBN', requires_grad=True)
# model = dict(
#     type='EncoderDecoder',
#     pretrained=None,
#     backbone=dict(
#         type='ConvNeXt',
#         in_chans=3,
#         depths=[3, 3, 9, 3],
#         dims=[96, 192, 384, 768],
#         drop_path_rate=0.2,
#         layer_scale_init_value=1.0,
#         out_indices=[0, 1, 2, 3],
#     ),
#     decode_head=dict(
#         type='UPerHead',
#         in_channels=[128, 256, 512, 1024],
#         in_index=[0, 1, 2, 3],
#         pool_scales=(1, 2, 3, 6),
#         channels=512,
#         dropout_ratio=0.1,
#         num_classes=19,
#         norm_cfg=norm_cfg,
#         align_corners=False,
#         loss_decode=dict(
#             type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0)),
#     auxiliary_head=dict(
#         type='FCNHead',
#         in_channels=384,
#         in_index=2,
#         channels=256,
#         num_convs=1,
#         concat_input=False,
#         dropout_ratio=0.1,
#         num_classes=19,
#         norm_cfg=norm_cfg,
#         align_corners=False,
#         loss_decode=dict(
#             type='CrossEntropyLoss', use_sigmoid=False, loss_weight=0.4)),
#     # model training and testing settings
#     train_cfg=dict(),
#     test_cfg=dict(mode='whole'))
