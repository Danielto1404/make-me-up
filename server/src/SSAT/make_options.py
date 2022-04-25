class MakeOptions:
    def __init__(
            self,
            *,
            dataroot='./test/images/',
            phase='test',
            input_dim=3,
            output_dim=3,
            semantic_dim=18,
            batch_size=1,
            resize_size=286,
            crop_size=256,
            flip=False,
            nThreads=8,
            name='makeup',
            display_dir='./logs',
            results_dir='./results',
            checkpoint_dir='./weights',
            display_freq=1,
            img_save_freq=1,
            model_save_freq=100,
            dis_scale=3,
            num_residual_block=4,
            lr=0.0002,
            device='cpu'
    ):
        self.dataroot = dataroot
        self.phase = phase
        self.input_dim = input_dim
        self.output_dim = output_dim
        self.semantic_dim = semantic_dim
        self.batch_size = batch_size
        self.resize_size = resize_size
        self.crop_size = crop_size
        self.flip = flip
        self.nThreads = nThreads
        self.name = name
        self.display_dir = display_dir
        self.result_dir = results_dir
        self.checkpoint_dir = checkpoint_dir
        self.display_freq = display_freq
        self.img_save_freq = img_save_freq
        self.model_save_freq = model_save_freq
        self.dis_scale = dis_scale
        self.num_residual_block = num_residual_block
        self.lr = lr
        self.device = device
