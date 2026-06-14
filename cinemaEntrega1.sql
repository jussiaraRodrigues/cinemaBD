DROP DATABASE IF EXISTS cinema;
CREATE DATABASE cinema;
USE cinema;

-- --------------------------------------------------------
-- Tabela: venda
-- 
CREATE TABLE venda (
    venda_id INT NOT NULL AUTO_INCREMENT,
    data_venda DATETIME NOT NULL,
    valor_total DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (venda_id)
);

-- --------------------------------------------------------
-- Tabela:filme
-- 
CREATE TABLE filme (
    filme_id INT NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(255) NOT NULL,
    duracao INT NOT NULL,
    classificacao VARCHAR(45) NOT NULL,
    PRIMARY KEY (filme_id)
);

-- --------------------------------------------------------
-- Tabela:sala
-- 
CREATE TABLE sala (
    sala_id INT NOT NULL AUTO_INCREMENT,
    nome VARCHAR(255) NOT NULL,
    capacidade INT NOT NULL,
    PRIMARY KEY (sala_id)
);

-- --------------------------------------------------------
-- Tabela: assento
-- 
CREATE TABLE assento (
    assento_id INT NOT NULL AUTO_INCREMENT,
    fila VARCHAR(2) NOT NULL,
    numero INT NOT NULL,
    sala_id INT NOT NULL,
    PRIMARY KEY (assento_id),
    UNIQUE KEY uk_assento (fila,numero,sala_id),
    KEY idx_fk_sala_id (sala_id)
);

-- --------------------------------------------------------
-- Tabela: sessao
-- 
CREATE TABLE sessao (
    sessao_id INT NOT NULL AUTO_INCREMENT,
    data_hora DATETIME NOT NULL,
    idioma VARCHAR(45) NOT NULL,
    filme_id INT NOT NULL,
    sala_id INT NOT NULL,
    PRIMARY KEY (sessao_id),
    KEY idx_fk_filme_id (filme_id),
    KEY idx_fk_sala_id (sala_id)
);

-- --------------------------------------------------------
-- Tabela: ingresso
-- 
CREATE TABLE ingresso (
    ingresso_id INT NOT NULL AUTO_INCREMENT,
    valor DECIMAL(10,2) NOT NULL,
    venda_id INT NOT NULL,
    sessao_id INT NOT NULL,
    assento_id INT NOT NULL,
    PRIMARY KEY (ingresso_id),
    KEY idx_fk_venda_id (venda_id),
    KEY idx_fk_sessao_id (sessao_id),
    KEY idx_fk_assento_id (assento_id)
);

-- --------------------------------------------------------
-- Restrições de Chaves Estrangeiras
-- 
ALTER TABLE assento
    ADD CONSTRAINT fk_assento_sala FOREIGN KEY (sala_id) REFERENCES sala (sala_id) ON UPDATE CASCADE;
    
ALTER TABLE sessao
    ADD CONSTRAINT fk_sessao_filme FOREIGN KEY (filme_id) REFERENCES filme (filme_id) ON UPDATE CASCADE,
    ADD CONSTRAINT fk_sessao_sala FOREIGN KEY (sala_id) REFERENCES sala (sala_id) ON UPDATE CASCADE;
    
ALTER TABLE ingresso
    ADD CONSTRAINT fk_ingresso_venda FOREIGN KEY (venda_id) REFERENCES venda (venda_id) ON UPDATE CASCADE,
    ADD CONSTRAINT fk_ingresso_sessao FOREIGN KEY (sessao_id) REFERENCES sessao (sessao_id) ON UPDATE CASCADE,
    ADD CONSTRAINT fk_ingresso_assento FOREIGN KEY (assento_id) REFERENCES assento (assento_id) ON UPDATE CASCADE;
