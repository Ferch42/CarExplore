# CarExplore
An environment for training agents that perform complete sweep exploration while learning to move at the same time

To run the environment just import the environment files:

```
from GoalEnvironment import GoalEnvironment
from GridEnvironment import GridEnvironment

env = GoalEnvironment()
env = GridEnvironment()

s = env.reset()
a = env.step(env.action_space.sample())
```

The GridEnvironment is the environment used for validation of the complete exploration

The GoalEnvironment may be used for training. 

In order to configure obstacles just add json files to the obstacles folder.

For more information please refer to https://drive.google.com/file/d/1oXPZzeguVCWX0lIh9jegFPW9GlIUnVIz/view?usp=sharing
