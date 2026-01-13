import torch
import timm
from torchvision import transforms
from PIL import Image

class GenderClassifier:
    def __init__(self, model_name='vit_tiny_patch16_224'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = timm.create_model(model_name, pretrained=True, num_classes=2)
        self.model.to(self.device)
        self.model.eval()

        self.classes = ['female', 'male']

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def load_model(self, model_path):
        checkpoint = torch.load(model_path, map_location=self.device)
        self.model.load_state_dict(checkpoint['model_state_dict'])

    def predict(self, image):
        image = Image.fromarray(image)
        image = self.transform(image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            output = self.model(image)
            probs = torch.softmax(output, dim=1)[0]
            conf, idx = torch.max(probs, dim=0)

        return self.classes[idx.item()], conf.item() * 100
