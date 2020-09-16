import argparse
import os
import torch
import json
import torch.nn.functional as F
import numpy as np
from pathlib import PurePath
from torchvision import transforms
from glob import glob
from PIL import Image
from simple_model import CNN_Net

parser = argparse.ArgumentParser()


def get_files_path(folder):
    extentions = ('*.jpg', '*.jpeg', '*.png')
    files = []
    for ext in extentions:
        files.extend(glob(str(PurePath(folder, ext))))
    return files


def normalize_div(tensor):
    return tensor.float() / 255.


def normalize_mean_std(tensor):
    tensor = tensor.float()
    tensor_copy = torch.Tensor.copy_(tensor)
    return (tensor - torch.mean(tensor_copy)) / torch.std(tensor_copy)


def get_model(model_type):
    if model_type == 'simple':
        model_params = {'img_size': 156, 'path': 'my_model_trained.pt',
                        'processing': transforms.Compose([transforms.Resize((156, 156)), transforms.ToTensor(),])}
    else:
        model_params = {'img_size': 224, 'path': 'vgg_model_trained.pt',
                        'processing': transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor(),
                                     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])}

    try:
        model = torch.load(model_params['path']) #.cpu()
    except FileNotFoundError as err:
        print(err)
        raise FileNotFoundError
    return model, model_params


def predict_images(paths, model, model_params):
    results = {}
    classes = {0: 'female', 1: 'male'}
    for img_path in paths:
        img = Image.open(img_path)
        img = img.convert("RGB")
        img = model_params['processing'](img)
        img = img.unsqueeze(0)
        with torch.no_grad():
            preds = F.softmax(model(img))
        results[img_path] = classes[int(torch.argmax(preds).item())]

    return results


if __name__ == '__main__':
    parser.add_argument('--folder', type=str, help="path to folder with images", required=True, dest='folder')
    parser.add_argument("-m", "--model", type=str, help="model type for predictions",
                        default="simple", dest="model_type", choices=["simple", "vgg"])

    args = vars(parser.parse_args())
    args['folder'] = PurePath(args['folder'])

    # check folder before load data and model
    if not os.path.isdir(args['folder']):
        raise NotADirectoryError('Folder not exists')

    paths = get_files_path(args['folder'])
    model, params = get_model(args['model_type'])
    results = predict_images(paths=paths, model=model, model_params=params)
    with open('results.json', mode='w') as f:
        json.dump(results, f, indent=4)