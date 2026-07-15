# DiffusionLab

DiffusionLab is a small Python library (with a handy command-line interface) for playing around with 2D lattice random walks. You can use it to calculate mean squared displacement (MSD) and estimate diffusion coefficients—pretty straightforward stuff.

All the commands in this README are given for **macOS**, but they'll likely work on Linux too with minor changes. I've tried to keep the code modular and tested, so you should be able to run it on any machine, not just the one I built it on. Reproducibility was a big focus as well.

## Project goal

The whole point of this project is to show something pretty fundamental: if you zoom out, all those tiny random movements at the microscopic level actually add up to smooth, predictable diffusion at the macroscopic scale.

Here's how it works in practice—I start a bunch of independent particles at the origin, let them hop around a 2D square lattice, and log where they end up. From those trajectories, I compute the average MSD across the ensemble, then fit a straight line through the data to back out the numerical diffusion coefficient.

## Scientific model

Here's the movement rule: at each step, a particle picks one of four directions—up, down, left, or right—all with equal chance.

```math
\Delta \mathbf{r} \in
\left\{
(a,0),\,(-a,0),\,(0,a),\,(0,-a)
\right\},
```

where $a$ is the step length.

For $N$ particles, the mean squared displacement from their initial positions is

```math
\mathrm{MSD}(t)
=
\frac{1}{N}
\sum_{i=1}^{N}
\left[
\left(x_i(t)-x_i(0)\right)^2
+
\left(y_i(t)-y_i(0)\right)^2
\right].
```

All particles in this implementation start at $(0,0)$, so this becomes

```math
\mathrm{MSD}(t)
=
\frac{1}{N}
\sum_{i=1}^{N}
\left[x_i^2(t)+y_i^2(t)\right].
```

For unrestricted diffusion in two dimensions,

```math
\mathrm{MSD}(t)=4Dt,
```

where $D$ is the diffusion coefficient.

For a lattice walk with step length $a$ and time interval $\Delta t$,

```math
\mathrm{MSD}(n)=na^2,
\qquad
t=n\Delta t,
```

and therefore

```math
D_{\mathrm{theory}}
=
\frac{a^2}{4\Delta t}.
```

The program fits the simulated data with

```math
\mathrm{MSD}(t)\approx mt+b
```

and estimates the diffusion coefficient from the fitted slope $m$:

```math
D_{\mathrm{estimated}}=\frac{m}{4}.
```

The intercept $b$ is not forced to zero. A small non-zero intercept is expected in a finite stochastic simulation.

## Main features

- **Reproducibility**:  set a seed, and the random walk is deterministic every time.
- **Configuration**: all settings go into a JSON file—no source-code editing required.
- **Boundary options**: choose between unrestricted or reflecting walls.
- **Modular code**: separate simulation, analysis, plotting, and I/O into their own modules.
- **Output formats**: get both CSV and JSON for your data.
- **Visualization**: the tool automatically spits out trajectory plots and MSD linear-fit figures.
- **CLI**: run everything from the command line if you prefer.
- **Testing**: include a suite of `pytest` tests to keep things stable.

## Requirements

- macOS
- Python 3.10 or newer
- NumPy 1.23 or newer
- pandas 1.5 or newer
- Matplotlib 3.6 or newer
- pytest 7 or newer for testing
- coverage.py 7 or newer for optional coverage measurement

Check the installed Python version:

```bash
python3 --version
```

If Python is not installed, install a current Python 3 release before continuing.

## Installation on macOS

Clone the public repository:

```bash
git clone https://github.com/mingqiuyang011/diffusionlab.git
cd diffusionlab
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

After activation, the terminal prompt should normally begin with `(.venv)`.

Upgrade `pip`:

```bash
python -m pip install --upgrade pip
```

Install the package and its development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Check that the installed dependencies are consistent:

```bash
python -m pip check
```

Check that the command-line interface is available:

```bash
diffusionlab --help
```

To leave the virtual environment later, run:

```bash
deactivate
```

## Quick start

Run the included free-diffusion example:

```bash
diffusionlab run --config configs/free_walk.json --out results/free_walk
```

> The current command-line interface uses `--config` and `--out` directly.

The command performs the complete workflow:

1. Load and validate the configuration.
2. Simulate the particle trajectories.
3. Calculate the MSD.
4. Fit the MSD curve and estimate $D$.
5. Save numerical outputs.
6. Generate the trajectory and MSD plots.

## Configuration

The example `configs/free_walk.json` contains:

```json
{
  "n_particles": 1000,
  "n_steps": 500,
  "step_length": 1.0,
  "time_step": 1.0,
  "seed": 42,
  "boundary": "none",
  "box_size": null,
  "save_every": 1
}
```

| Parameter       | Description                                    | Valid value                                           |
| --------------- | ---------------------------------------------- | ----------------------------------------------------- |
| `n_particles` | Number of independent particles                | Positive integer                                      |
| `n_steps`     | Number of random-walk steps                    | Positive integer                                      |
| `step_length` | Lattice step length$a$                       | Positive number                                       |
| `time_step`   | Time interval$\Delta t$ per step             | Positive number                                       |
| `seed`        | Random seed used for reproducibility           | Integer                                               |
| `boundary`    | Boundary condition                             | `"none"` or `"reflecting"`                        |
| `box_size`    | Side length of the reflecting square           | Positive for a reflecting boundary; otherwise`null` |
| `save_every`  | Save one state every specified number of steps | Positive integer                                      |

Invalid user-facing parameters are rejected with informative exceptions.

## Generated output

The quick-start command creates:

```text
results/free_walk/
├── trajectories.csv
├── msd.csv
├── summary.json
├── trajectories.png
└── msd_fit.png
```

| File                 | Contents                                                                                   |
| -------------------- | ------------------------------------------------------------------------------------------ |
| `trajectories.csv` | Position of every particle at every saved step                                             |
| `msd.csv`          | Simulation step, physical time, and MSD                                                    |
| `summary.json`     | Fit parameters, estimated and theoretical$D$, relative error, and configuration metadata |
| `trajectories.png` | Sample particle trajectories                                                               |
| `msd_fit.png`      | Simulated MSD and its fitted line                                                          |

Generated result files are ignored by Git because they can be reproduced from the configuration and source code. Two small example figures are stored in `docs/images/` for display in this README.

## Example result

The displayed example was generated with:

| Setting               | Value |
| --------------------- | ----: |
| Number of particles   |  1000 |
| Number of steps       |   500 |
| Step length$a$      |   1.0 |
| Time step$\Delta t$ |   1.0 |
| Random seed           |    42 |
| Boundary condition    |  None |

For these parameters,

```math
D_{\mathrm{theory}}
=
\frac{1^2}{4(1)}
=
0.25.
```

The generated `summary.json` contains:

| Quantity              |        Result |
| --------------------- | ------------: |
| Fitted slope$m$     |  1.0113316342 |
| Fitted intercept$b$ | -0.4918985773 |
| Estimated$D=m/4$    |  0.2528329086 |
| Theoretical$D$      |  0.2500000000 |
| Relative error        |       1.1332% |

The numerical estimate is close to the theoretical value. The difference is expected because the MSD is calculated from a finite ensemble of random trajectories.

The final recorded MSD at $t=500$ is `506.926`, while the theoretical ensemble expectation is `500`.

### Example particle trajectories

![Sample trajectories of the two-dimensional random walkers](docs/images/trajectories.png)

Individual trajectories are irregular. The diffusion law appears only after averaging over the ensemble of particles.

### MSD and linear fit

![Mean squared displacement and fitted diffusion line](docs/images/msd_fit.png)

The approximately linear MSD curve is consistent with unrestricted diffusion. The fitted slope is used to estimate $D$.

## Additional experiments

### Effect of step length

Run the included configurations:

```bash
diffusionlab --config configs/step_length_05.json --out results/step_length_05
diffusionlab --config configs/step_length_20.json --out results/step_length_20
```

For fixed $\Delta t=1$, theory predicts:

| Step length$a$ | Theoretical$D=a^2/(4\Delta t)$ |
| ---------------: | -------------------------------: |
|              0.5 |                           0.0625 |
|              1.0 |                             0.25 |
|              2.0 |                              1.0 |

Thus,

```math
D\propto a^2.
```

### Reflecting boundary

Run the confined example:

```bash
diffusionlab --config configs/reflecting_box.json --out results/reflecting_box
```

With reflective walls in place, the walkers never leave the box. You'll see the MSD rise at first, then the growth tapers off and it levels out—basically hits a ceiling.

The free-space relation $\mathrm{MSD}=4Dt$ applies only before confinement dominates. A linear fit over the entire confined trajectory should therefore not be interpreted as a free-space diffusion coefficient.

## Testing on macOS

Activate the project environment before running tests:

```bash
source .venv/bin/activate
```

Run the full test suite:

```bash
pytest -v
```

The current test suite includes 11 tests that cover the following:

- Configuration files are loaded and validated against the expected schema.
- All particles are initialized at the origin at the start of each simulation.
- The step length is confirmed to equal the prescribed lattice spacing.
- Using a fixed random seed yields bitwise-identical trajectories across runs.
- Reflecting boundaries keep particles inside the finite square, with proper bounce behavior.
- The MSD calculation is checked against reference values computed by hand.
- The diffusion‑coefficient fitting routine recovers the correct slope from synthetic linear data.
- Both CSV and JSON I/O functions are exercised to ensure correct read/write operations.

Measure coverage with:

```bash
coverage erase
coverage run -m pytest
coverage report -m
```

Tests should pass before a commit is submitted.

## Project structure

```text
diffusionlab/
├── diffusionlab/
│   ├── __init__.py
│   ├── config.py
│   ├── random_walk.py
│   ├── analysis.py
│   ├── plotting.py
│   ├── io.py
│   └── cli.py
├── tests/
│   ├── test_config.py
│   ├── test_random_walk.py
│   ├── test_analysis.py
│   └── test_io.py
├── configs/
│   ├── free_walk.json
│   ├── step_length_05.json
│   ├── step_length_20.json
│   └── reflecting_box.json
├── docs/
│   └── images/
│       ├── trajectories.png
│       └── msd_fit.png
├── results/                 # generated locally and ignored by Git
├── figures/                 # generated locally and ignored by Git
├── README.md
├── pyproject.toml
├── .gitignore
└── LICENSE
```

The modules and their responsibilities:

- `config.py` handles loading and validation of user‑supplied parameters.
- `random_walk.py` runs the simulation itself—stepping particles on the lattice one move at a time.
- `analysis.py` computes the ensemble MSD and fits a linear regression to extract the diffusion coefficient.
- `io.py` manages all reading and writing of numerical results, including both CSV and JSON formats.
- `plotting.py` is reserved exclusively for generating figures (trajectory plots and MSD‑fit curves).
- `cli.py` ties together the other modules into a single command‑line workflow for the end user.

## Reproducibility

A run is defined by:

1. The JSON configuration.
2. The random seed.
3. The documented dependency versions.
4. The command-line invocation.

Using the same configuration and seed produces the same simulated trajectories with compatible dependency versions. The source code contains no machine-specific absolute paths.

## Clean-clone verification on macOS

The following procedure simulates installation on another machine:

```bash
cd ..
rm -rf diffusionlab_clean_test
git clone https://github.com/mingqiuyang011/diffusionlab.git diffusionlab_clean_test
cd diffusionlab_clean_test
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pip check
pytest -v
diffusionlab --config configs/free_walk.json --out results/clean_test
```

Inspect the generated files:

```bash
ls -lh results/clean_test
python -m json.tool results/clean_test/summary.json
```

Check the documentation images:

```bash
test -f docs/images/trajectories.png && echo "trajectories image: OK"
test -f docs/images/msd_fit.png && echo "MSD image: OK"
```

## Limitations

Current limitations of the model include:

- Motion is restricted to a discrete square lattice, rather than continuous Brownian paths.
- Particles are treated as independent—they do not collide or interact with one another.
- Several physical effects are not accounted for: external forces, hydrodynamic interactions, and spatial variations in the diffusion coefficient.
- Statistical accuracy improves with more particles, but that comes with increased runtime, memory usage, and output file size.
- Storage requirements scale linearly with the number of particles and the number of saved time steps.
- The diffusion coefficient obtained from a linear fit is only valid for free diffusion; after a reflecting-boundary simulation enters the confined regime, that fit no longer applies.

## Author

mingqiuyang011

## License

See the `LICENSE` file for the terms under which this project may be used.
