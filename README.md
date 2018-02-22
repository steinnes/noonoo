![image](https://user-images.githubusercontent.com/1097582/36531350-6f72a148-17b5-11e8-8a0b-0da69bd3217e.png)

# noonoo

Tool to clean up Elastic Container Repositories in AWS.


## Setup

    $ pip install noonoo

Noonoo uses AWS boto, so it will pickup AWS credentials via `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables, or via `~/.aws`. See [boto3 configuration](https://boto3.readthedocs.io/en/latest/guide/configuration.html) for details.


## Usage

    $ noonoo --help
    Usage: noonoo [OPTIONS] REPOSITORY

      Clean up older/untagged images from an ECR.

    Options:
      --region TEXT      The AWS region of the ECS repository
      --remove_untagged  Remove all images without tags
      --keep INTEGER     How many old images to keep
      --prompt           Prompt before deleting
      -n, --dryrun       Only print intentions
      --help             Show this message and exit.


## Example

    $ noonoo my-repo-name --region=us-east-1 --prompt --keep 5
    Found 100 images in ECR, will keep 5
    Continue? [y/N]: y
    keeping: [2018-02-21T15:37:02+00:00: {'imageTag': u'git_b8632d12e9488e49bbf8e90dc0b8cf9c2351d952', 'imageDigest': u'sha256:fda784c13cf1ece902a22508beb174a28930caf2b87c764cffed51aa556d5c9c'}]
    keeping: [2018-02-21T15:25:45+00:00: {'imageTag': u'git_911b312edac670cc0d58b7885019a3f28461ba5c', 'imageDigest': u'sha256:f5ed39608c0b1b49afeadcdcff3e96c1aedfdc5809cf12a78d83214c2622af9a'}]
    keeping: [2018-02-21T14:56:36+00:00: {'imageTag': u'git_ccb5319b463936f8610f046b4d7b6a0186beaf68', 'imageDigest': u'sha256:69ace0b7a222aa537e8233854d446bf86d9da895629c69eb84349814484f573d'}]
    keeping: [2018-02-21T13:20:07+00:00: {'imageTag': u'git_111e5e59ece155b6a52c870881ae33d0ed41c7b8', 'imageDigest': u'sha256:705f2f1558bb5438531d3c24593e5d9c04bddd60e7f9de1a2dd2a782f31f0bb7'}]
    keeping: [2018-02-21T12:11:42+00:00: {'imageTag': u'git_f8a71ecebe2c985999baa551b738391679dbce0b', 'imageDigest': u'sha256:4f9a6e855885d929ba10d9b021db0cf12625646356e4ed9cf0e2df6bc1979107'}]
    Deleting: 95
    Done, deleted


## Background

At [Takumi](https://github.com/TakumiHQ) we push app container images into ECR's as part of our CI process.  These ECR's have the standard size limit of 1000 images, and when they fill up our CI pipeline breaks. Noonoo
is a repackaged version of a janitor script I wrote for some internal deployment tools we're no longer using.

The name is lifted from "Noo-Noo", a character on the BBC children's television show Teletubbies.  The [Wikipedia](https://en.wikipedia.org/wiki/Teletubbies#Supporting_characters) description says it best:
*The Noo-noo is a conscientious vacuum cleaner who acts as both the Teletubbies' guardian and housekeeper. He hardly ever ventures outside the Tubbytronic Superdome, instead remaining indoors and constantly cleaning with his sucker-like nose. He communicates through a series of slurping and sucking noises.*
