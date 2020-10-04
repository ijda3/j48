#!/usr/bin/env python
import pdb

from j48.main import Main

j48 = Main()
j48.setAtributos('../datasets/heart_failure/attributes')
j48.setData('../datasets/heart_failure/data')
j48.gerarArvore()
j48.exibirArvore()
