import numpy as np


def gen_data(size, is_short):
    X = np.array(np.random.choice(2, size=(size,)))
    Y = []
    if is_short:
        x_min = 5
        x_max = 12
    else:
        x_min = 15
        x_max = 30

    for i in range(size):
        threshold = 0.5
        if X[i-x_min] == 1:
            threshold += 0.5
        if X[i-x_max] == 1:
            threshold -= 0.25
        if np.random.rand() > threshold:
            Y.append(0)
        else:
            Y.append(1)
    return X, np.array(Y)


def gen_batch(raw_data, batch_size, num_steps):
    raw_x, raw_y = raw_data
    data_length = len(raw_x)

    # partition raw data into batches and stack them vertically in a data matrix
    batch_partition_length = data_length // batch_size
    data_x = np.zeros([batch_size, batch_partition_length], dtype=np.int32)
    data_y = np.zeros([batch_size, batch_partition_length], dtype=np.int32)
    for i in range(batch_size):
        data_x[i] = raw_x[batch_partition_length * i:batch_partition_length * (i + 1)]
        data_y[i] = raw_y[batch_partition_length * i:batch_partition_length * (i + 1)]
    # further divide batch partitions into num_steps for truncated backprop
    epoch_size = batch_partition_length // num_steps

    for i in range(epoch_size):
        x = data_x[:, i * num_steps:(i + 1) * num_steps]
        y = data_y[:, i * num_steps:(i + 1) * num_steps]
        yield (x, y)


def gen_epochs(n, batch_size, num_steps):
    for i in range(n):
        yield gen_batch(gen_data(), batch_size, num_steps)


if __name__ == "__main__":
    X,Y = gen_data()
    print(np.shape(X))
    print(np.shape(Y))



