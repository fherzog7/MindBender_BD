#!/bin/bash

git add .
echo "Enter a comment:"
read comment
git commit -m "$comment"
git push -u origin main