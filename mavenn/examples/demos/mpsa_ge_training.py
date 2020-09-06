"""
demo: mpsa_ge_training

Trains a neighbor G-P map, using GE regression with
a homoskedastic Gaussian noise model, on data from
Wong et al., 2018. Takes ~15 seconds to run.
"""

# Standard imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time

# Import MAVE-NN and a dataset splitter from sklearn
import mavenn
from sklearn.model_selection import train_test_split

# Load dataset as a dataframe
data_df = pd.read_csv(mavenn.__path__[0] +
                      '/examples/datafiles/mpsa/brca2_lib1_rep1.csv')

# Extract x and y as np.arrays
x = data_df['ss'].values
y = data_df['log_psi'].values

# Split into training and test sets
x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=0)

# Define model and set training data
model = mavenn.Model(x=x_train,
                     y=y_train,
                     gpmap_type='neighbor',
                     alphabet='dna',
                     regression_type='GE',
                     ge_noise_model_type='Gaussian',
                     ge_nonlinearity_monotonic=True,
                     ge_heteroskedasticity_order=0)

# Fit model to training data
start_time = time.time()
model.fit(epochs=20,
          learning_rate=0.002,
          early_stopping=False,
          validation_split=0.1,
          verbose=True)
training_time = time.time()-start_time
print(f'training time: {training_time}')

# Predict latent phentoype values (phi) on test data
phi_test = model.x_to_phi(x_test)

# Predict measurement values (yhat) on test data
yhat_test = model.x_to_yhat(x_test)

# Compute R^2 between yhat and y_test
Rsq = np.corrcoef(yhat_test.ravel(), y_test)[0, 1]**2

# Set phi lims and create grid in phi space
phi_lim = [min(phi_test)-.5, max(phi_test)+.5]
phi_grid = np.linspace(phi_lim[0], phi_lim[1], 1000)

# Compute yhat each phi gridpoint
yhat_grid = model.phi_to_yhat(phi_grid)

# Compute 68% CI for each yhat
yqs_grid = model.yhat_to_yq(yhat_grid,
                            q=[0.16,0.84])

# Extract training loss and validation loss
history_dict = model.model.history.history
loss_training = history_dict['loss']
loss_validation = history_dict['val_loss']

# Create figure and axes
fig, axs = plt.subplots(1, 3, figsize=[12, 4])

# Left panel: illustrate measurement process (y vs. phi)
ax = axs[0]
ax.scatter(phi_test, y_test, color='C0', s=5, alpha=.2, label='test data')
ax.plot(phi_grid, yhat_grid, linewidth=2, color='C1',
        label='$\hat{y} = g(\phi)$')
ax.plot(phi_grid, yqs_grid[:,0], linestyle='--', color='C1', label='68% CI')
ax.plot(phi_grid, yqs_grid[:,1], linestyle='--', color='C1')
ax.set_xlim(phi_lim)
ax.set_xlabel('latent phenotype ($\phi$)')
ax.set_ylabel('measurement ($y$)')
ax.set_title('measurement process')
ax.legend()

# Center panel: illustrate model performance (y vs. yhat)
ax = axs[1]
ys = np.vstack([y_test])
ax.scatter(yhat_test, y_test, color='C0', s=5, alpha=.2, label='test data')
ax.set_autoscale_on(False)
lims = ax.get_xlim()
ax.plot(lims, lims, linestyle=':', color='k', label='$y=\hat{y}$')
ax.set_xlabel('model prediction ($\hat{y}$)')
ax.set_ylabel('measurement ($y$)')
ax.set_title(f'performance ($R^2$={Rsq:.3})')
ax.legend()

# Right panel: Plot model training history
ax = axs[2]
ax.plot(loss_training, color='C2', label='training')
ax.plot(loss_validation, color='C3', label='validation')
ax.set_ylabel('loss')
ax.set_xlabel('epoch')
ax.set_title(f"training history ({training_time:.2f} sec)")
ax.legend()

# Tighten bounds on figure
fig.tight_layout(w_pad=3)