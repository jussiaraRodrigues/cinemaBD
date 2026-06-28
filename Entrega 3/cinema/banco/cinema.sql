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
-- Tabela: filme
-- 
CREATE TABLE filme (
    filme_id INT NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(255) NOT NULL,
    duracao INT NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    classificacao VARCHAR(45) NOT NULL,
    PRIMARY KEY (filme_id)
);

-- --------------------------------------------------------
-- Tabela: sala
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
    venda_id INT NULL,
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

-- --------------------------------------------------------
-- Regras de Negócio
-- --------------------------------------------------------

DELIMITER $$
-- --------------------------------------------------------
-- Procedure de cadastro de sala + assentos
-- 
CREATE PROCEDURE sp_cadastrar_sala_com_assentos(
    IN p_nome VARCHAR(255),
    IN p_capacidade_total INT,
    IN p_qtd_filas INT,
    IN p_assentos_por_fila INT
)
BEGIN
    DECLARE v_sala_id INT;
    DECLARE v_fila_atual INT DEFAULT 0;
    DECLARE v_assento_atual INT DEFAULT 1;
    DECLARE v_letra_fila VARCHAR(2);

    INSERT INTO sala (nome, capacidade) 
    VALUES (p_nome, p_capacidade_total);
    
    SET v_sala_id = LAST_INSERT_ID();

    WHILE v_fila_atual < p_qtd_filas DO
        SET v_letra_fila = CHAR(65 + v_fila_atual);
        
        SET v_assento_atual = 1;
        
        WHILE v_assento_atual <= p_assentos_por_fila DO
            INSERT INTO assento (fila, numero, sala_id) 
            VALUES (v_letra_fila, v_assento_atual, v_sala_id);
            
            SET v_assento_atual = v_assento_atual + 1;
        END WHILE;
        
        SET v_fila_atual = v_fila_atual + 1;
    END WHILE;
END$$

-- --------------------------------------------------------
-- Procedure de deletar sala + assentos
-- 
CREATE PROCEDURE sp_deletar_sala(
    IN p_sala_id INT
)
BEGIN
    DELETE FROM assento WHERE sala_id = p_sala_id;
    
    DELETE FROM sala WHERE sala_id = p_sala_id;
END$$

-- --------------------------------------------------------
-- Procedure de cadastro de filme
-- 
CREATE PROCEDURE sp_cadastrar_filme(
    IN p_titulo VARCHAR(255),
    IN p_duracao INT,
    IN p_categoria VARCHAR(100),
    IN p_classificacao VARCHAR(45)
)
BEGIN
    INSERT INTO filme (titulo, duracao, categoria, classificacao)
    VALUES (p_titulo, p_duracao, p_categoria, p_classificacao);
END$$

-- --------------------------------------------------------
-- Procedure de deletar filme
-- 
CREATE PROCEDURE sp_deletar_filme(
    IN p_filme_id INT
)
BEGIN
    DELETE FROM ingresso 
    WHERE sessao_id IN (SELECT sessao_id FROM sessao WHERE filme_id = p_filme_id);
    
    DELETE FROM sessao WHERE filme_id = p_filme_id;
    
    DELETE FROM filme WHERE filme_id = p_filme_id;
END$$

-- --------------------------------------------------------
-- Procedure de cadastro de sessão + ingressos
-- 
CREATE PROCEDURE sp_criar_sessao_e_gerar_ingressos(
    IN p_data_hora DATETIME,
    IN p_idioma VARCHAR(45),
    IN p_filme_id INT,
    IN p_sala_id INT,
    IN p_valor_ingresso DECIMAL(10,2)
)
BEGIN
    DECLARE v_sessao_id INT;
    
    INSERT INTO sessao (data_hora, idioma, filme_id, sala_id)
    VALUES (p_data_hora, p_idioma, p_filme_id, p_sala_id);
    
    SET v_sessao_id = LAST_INSERT_ID();
    
    INSERT INTO ingresso (valor, venda_id, sessao_id, assento_id)
    SELECT p_valor_ingresso, NULL, v_sessao_id, assento_id
    FROM assento
    WHERE sala_id = p_sala_id;
    
END$$

-- --------------------------------------------------------
-- Procedure de deletar sessão
-- 
CREATE PROCEDURE sp_deletar_sessao(
    IN p_sessao_id INT
)
BEGIN
    DELETE FROM ingresso WHERE sessao_id = p_sessao_id;
    
    DELETE FROM sessao WHERE sessao_id = p_sessao_id;
END$$

-- --------------------------------------------------------
-- Procedure de cadastro de venda
-- 
CREATE PROCEDURE sp_fazer_venda(
    IN p_venda_id INT,
    IN p_ingresso_id INT,
    IN p_valor DECIMAL(10,2)
)
BEGIN
    INSERT INTO venda (venda_id, data_venda, valor_total) 
    VALUES (p_venda_id, NOW(), p_valor);

    UPDATE ingresso 
    SET venda_id = p_venda_id 
    WHERE ingresso_id = p_ingresso_id;
END$$

-- --------------------------------------------------------
-- Procedure de cancelar venda
-- 
CREATE PROCEDURE sp_cancelar_venda(
    IN p_venda_id INT
)
BEGIN
    UPDATE ingresso 
    SET venda_id = NULL 
    WHERE venda_id = p_venda_id;

    DELETE FROM venda 
    WHERE venda_id = p_venda_id;
END$$

-- --------------------------------------------------------
-- Função para verificar se o ingresso foi vendido
-- 
CREATE FUNCTION fn_ingresso_vendido(p_ingresso_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE v_venda_id INT;

    SELECT venda_id INTO v_venda_id
    FROM ingresso
    WHERE ingresso_id = p_ingresso_id;

    IF v_venda_id IS NULL THEN
        RETURN 0;
    ELSE
        RETURN 1;
    END IF;
END$$

-- --------------------------------------------------------
-- Função para verificar quantidade de ingressos vendidos
-- 
CREATE FUNCTION fn_ingressos_vendidos(
    p_sessao_id INT
)
RETURNS INT
DETERMINISTIC
BEGIN

    DECLARE v_total INT;

    SELECT COUNT(*)
    INTO v_total
    FROM ingresso
    WHERE sessao_id = p_sessao_id
      AND venda_id IS NOT NULL;

    RETURN v_total;

END $$

-- --------------------------------------------------------
-- Tigger para não permir compara de ingressos quando a sessão já passou
-- 
CREATE TRIGGER tg_bloqueia_ingresso_retroativo_update
BEFORE UPDATE ON ingresso
FOR EACH ROW
BEGIN
    DECLARE v_data_venda DATETIME;
    DECLARE v_data_sessao DATETIME;

    IF NEW.venda_id IS NOT NULL AND (OLD.venda_id IS NULL OR NEW.venda_id <> OLD.venda_id) THEN
        
        SELECT data_venda INTO v_data_venda 
        FROM venda 
        WHERE venda_id = NEW.venda_id; 

        SELECT data_sessao INTO v_data_sessao 
        FROM sessao 
        WHERE sessao_id = NEW.sessao_id; 

        IF v_data_venda > v_data_sessao THEN
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Esta sessão já ocorreu! Não é possível vender ingressos para ela.';
        END IF;
        
    END IF;
END$$

DELIMITER ;

-- --------------------------------------------------------
-- View para saber quais sessões estão livres e quantas vagas disponiveis
-- 
CREATE VIEW vw_sessoes_e_vagas AS
SELECT 
    s.sessao_id,
    f.titulo AS filme,
    s.data_hora,
    s.idioma,
    
    COUNT(CASE WHEN i.venda_id IS NULL THEN 1 END) AS vagas_disponiveis
FROM sessao s
INNER JOIN filme f ON s.filme_id = f.filme_id
LEFT JOIN ingresso i ON s.sessao_id = i.sessao_id
GROUP BY s.sessao_id, f.titulo, s.data_hora, s.idioma;

-- --------------------------------------------------------
-- View para saber quais assentos de uma sessão estão livres
-- 
CREATE VIEW vw_mapa_assentos_sessao AS
SELECT 
    i.sessao_id,
    i.ingresso_id,
    i.valor,
    a.fila,
    a.numero,

    CASE 
        WHEN i.venda_id IS NULL THEN 'Livre'
        ELSE 'Ocupado'
    END AS situacao
FROM ingresso i
INNER JOIN assento a ON i.assento_id = a.assento_id;

-- --------------------------------------------------------
-- View de histórico de vendas
-- 
CREATE VIEW vw_historico_vendas AS
SELECT 
    v.venda_id,
    v.data_venda,
    v.valor_total AS valor_total_venda,
    i.ingresso_id,
    f.titulo AS filme,
    s.data_hora AS data_hora_sessao,
    sa.nome AS sala,
    a.fila,
    a.numero AS numero_assento,
    i.valor AS valor_ingresso
FROM venda v
INNER JOIN ingresso i ON v.venda_id = i.venda_id
INNER JOIN sessao s ON i.sessao_id = s.sessao_id
INNER JOIN filme f ON s.filme_id = f.filme_id
INNER JOIN sala sa ON s.sala_id = sa.sala_id
INNER JOIN assento a ON i.assento_id = a.assento_id;

-- --------------------------------------------------------
-- View de capacidade de salas
-- 
CREATE VIEW vw_salas AS
SELECT
    s.sala_id,
    s.nome,
    s.capacidade,
    COUNT(DISTINCT a.fila) AS filas,
    MAX(a.numero) AS assentos_por_fila
FROM sala s
INNER JOIN assento a
    ON s.sala_id = a.sala_id
GROUP BY
    s.sala_id,
    s.nome,
    s.capacidade;
    
-- --------------------------------------------------------
-- View da sessão com dados + vendidos
-- 
CREATE VIEW vw_sessoes AS
SELECT
    s.sessao_id,
    f.titulo,
    sa.nome,
    sa.capacidade,
    s.data_hora,
    s.idioma,
    fn_ingressos_vendidos(s.sessao_id) AS vendidos,
    sa.capacidade - fn_ingressos_vendidos(s.sessao_id) AS disponiveis
FROM sessao s

INNER JOIN filme f
ON s.filme_id = f.filme_id

INNER JOIN sala sa
ON s.sala_id = sa.sala_id;