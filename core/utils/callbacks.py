from lightning.pytorch import Callback
from flask_socketio import SocketIO, emit
from pathlib import Path
import pickle

class TrainingProgressCallback(Callback):
    def __init__(self, socketio: SocketIO, project_path: str | Path):
        super().__init__()
        self.socketio = socketio
        self.project_path = project_path if isinstance(project_path, Path) else Path(project_path)
        self.log_path = self.project_path / "log"
        self.log_path.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_path / "training_log.txt"
        self.loss_metrics = {
            "epoch": [],
        }
    
    def on_train_epoch_start(self, trainer, pl_module):
        epoch = trainer.current_epoch
        total_epochs = trainer.max_epochs
        self.socketio.emit('training_progress', {
            'epoch': epoch,
            'total_epochs': total_epochs,
            'training_complete': False,
            'inference_complete': False
        })
    
    def on_train_epoch_end(self, trainer, pl_module):
        epoch = trainer.current_epoch
        # loss = trainer.logged_metrics.get("train_loss", 0)
        loss_metrics = {key: value.item() for key, value in trainer.logged_metrics.items() if "loss" in key and "step" not in key}
        total_epochs = trainer.max_epochs

        self.loss_metrics["epoch"].append(epoch)
        for key, value in loss_metrics.items():
            if key not in self.loss_metrics:
                self.loss_metrics[key] = []
            self.loss_metrics[key].append(value)
        
        # Save loss metrics to log file
        if not self.log_file.exists():
            with open(self.log_file, "wt") as f:
                f.write("epoch\t" + "\t".join(loss_metrics.keys()) + "\n")
                f.write(f"{epoch}\t" + "\t".join([str(value) for value in loss_metrics.values()]) + "\n")
        else:
            with open(self.log_file, "a") as f:
                f.write(f"{epoch}\t" + "\t".join([str(value) for value in loss_metrics.values()]) + "\n")

        self.socketio.emit('training_progress', {
            'epoch': epoch,
            'loss': loss_metrics,
            'total_epochs': total_epochs,
            'training_complete': False,
            'inference_complete': False
        })
    
    def on_train_end(self, trainer, pl_module):
        self.socketio.emit('training_progress', {
            'training_complete': True,
            'inference_complete': False
        })

        with open(self.log_path / "loss_metrics.pkl", "wb") as f:
            pickle.dump(self.loss_metrics, f)
    
    # def on_predict_batch_end(self, trainer, pl_module, outputs, batch, batch_idx, dataloader_idx = 0):
    #     if isinstance(trainer.predict_dataloaders, list):
    #         total_batchs = len(trainer.predict_dataloaders[0])
    #     else:
    #         total_batchs = len(trainer.predict_dataloaders)
    #     self.socketio.emit('training_progress', {
    #         'epoch': batch_idx + 1,
    #         'total_epochs': total_batchs,
    #         'training_complete': True,
    #         'inference_complete': False
    #     })
    def on_predict_epoch_start(self, trainer, pl_module):
        epoch = trainer.current_epoch
        total_epochs = trainer.max_epochs
        self.socketio.emit('training_progress', {
            'epoch': epoch,
            'total_epochs': total_epochs,
            'training_complete': True,
            'inference_complete': False
        })
    
    def on_predict_end(self, trainer, pl_module):
        self.socketio.emit('training_progress', {
            'training_complete': True,
            'inference_complete': True,
            'project_path': str(self.project_path)
        })

class InferenceProgressCallback(Callback):
    def __init__(self, socketio: SocketIO, test_path: str | Path):
        self.socketio = socketio
        self.test_path = test_path if isinstance(test_path, Path) else Path(test_path)
        super().__init__()
    
    def on_predict_epoch_start(self, trainer, pl_module):
        epoch = trainer.current_epoch
        total_epochs = trainer.max_epochs
        self.socketio.emit('training_progress', {
            'epoch': epoch,
            'total_epochs': total_epochs,
            'training_complete': True,
            'inference_complete': False
        })
    
    def on_predict_end(self, trainer, pl_module):
        self.socketio.emit('training_progress', {
            'training_complete': True,
            'inference_complete': True,
            'test_path': str(self.test_path)
        })