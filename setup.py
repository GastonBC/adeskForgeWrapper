from distutils.core import setup
setup(
  name = 'adeskForgeWrapper',
  packages = ['adeskForgeWrapper'],
  version = 'v1.2.1',
  license='MIT',
  description = 'Python wrapper for Autodesks Forge API',
  author = 'Gaston Balparda',
  author_email = 'gastonbalparda@gmail.com',
  url = 'https://github.com/GastonBC/adeskForgeWrapper',
  download_url = 'https://github.com/GastonBC/adeskForgeWrapper/archive/v1.2.1.tar.gz',
  keywords = ["python", "autodesk", "forge", "wrapper"],
  install_requires=[            # I get to this in a second
          'requests'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)