CREATE DATABASE IF NOT EXISTS correcao_enem;
USE correcao_enem;

CREATE TABLE IF NOT EXISTS redacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    redacao VARCHAR(255) NOT NULL,
    C1 INT NOT NULL,
    C2 INT NOT NULL,
    C3 INT NOT NULL,
    C4 INT NOT NULL,
    C5 INT NOT NULL,
    nota_final INT NOT NULL
);

-- Inserindo os dados com as notas (substitua os zeros pelos valores reais)
INSERT INTO redacoes (redacao, C1, C2, C3, C4, C5, nota_final) VALUES 
('redacao_01.jpg', 120, 120, 120, 120, 120, 600),
('redacao_02.jpg', 120, 120, 120, 120, 120, 600),
('redacao_03.jpg', 80, 80, 80, 80, 0, 320),
('redacao_04.jpg', 80, 120, 80, 80, 80, 440),
('redacao_05.jpg', 40, 80, 80, 80, 0, 280),
('redacao_06.jpg', 120, 80, 80, 80, 0, 360),
('redacao_07.jpg', 120, 80, 120, 120, 40, 440),
('redacao_08.jpg', 40, 40, 40, 40, 0, 160),
('redacao_09.jpg', 80, 120, 80, 80, 40, 400),
('redacao_10.jpg', 80, 80, 80, 80, 80, 400),
('redacao_11.jpg', 120, 120, 120, 120, 80, 560),
('redacao_12.jpg', 80, 120, 80, 80, 40, 400),
('redacao_13.jpg', 200, 200, 200, 200, 200, 1000),
('redacao_15.jpg', 200, 200, 200, 200, 200, 1000);