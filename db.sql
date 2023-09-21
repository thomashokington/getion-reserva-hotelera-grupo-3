-- Creación de la tabla de Hoteles
CREATE TABLE Hoteles (
    hotel_id serial PRIMARY KEY,
    nombre VARCHAR(255),
    ubicacion VARCHAR(255),
    descripcion TEXT,
    estrellas INTEGER
);

-- Creación de la tabla de Tipos de Habitación
CREATE TABLE TiposDeHabitacion (
    tipo_id serial PRIMARY KEY,
    nombre VARCHAR(255),
    descripcion TEXT,
    precio_base DECIMAL(10, 2)
);

-- Creación de la tabla de Habitaciones
CREATE TABLE Habitaciones (
    habitacion_id serial PRIMARY KEY,
    hotel_id INTEGER REFERENCES Hoteles(hotel_id),
    tipo_id INTEGER REFERENCES TiposDeHabitacion(tipo_id),
    numero VARCHAR(20),
    disponible BOOLEAN
);

-- Creación de la tabla de Clientes
CREATE TABLE Clientes (
    cliente_id serial PRIMARY KEY,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    correo VARCHAR(255),
    telefono VARCHAR(20)
);

-- Creación de la tabla de Reservas
CREATE TABLE Reservas (
    reserva_id serial PRIMARY KEY,
    cliente_id INTEGER REFERENCES Clientes(cliente_id),
    habitacion_id INTEGER REFERENCES Habitaciones(habitacion_id),
    fecha_entrada DATE,
    fecha_salida DATE,
    precio_total DECIMAL(10, 2)
);

INSERT INTO Hoteles (nombre, ubicacion, descripcion, estrellas)
VALUES
    ('Hotel Tajamar', 'Concepción', 'Un hotel de lujo en el centro de la ciudad.', 5),
    ('Hotel Pacific Reef', 'Viña del Mar', 'Un resort frente al mar con todas las comodidades.', 4),
    ('Hotel Miramax', 'Los Andes', 'Un refugio acogedor en las montañas.', 3);

INSERT INTO TiposDeHabitacion (nombre, descripcion, precio_base)
VALUES
    ('Individual', 'Una habitación individual con cama individual.', 100.00),
    ('Doble', 'Una habitación doble con cama queen-size o king-size.', 150.00),
    ('Suite', 'Una suite de lujo con sala de estar y bañera de hidromasaje.', 250.00);

-- Habitaciones en el Hotel Ejemplo 1
INSERT INTO Habitaciones (hotel_id, tipo_id, numero, disponible)
VALUES
    (1, 1, '101', true),
    (1, 2, '102', true),
    (1, 2, '103', false);

-- Habitaciones en el Hotel Ejemplo 2
INSERT INTO Habitaciones (hotel_id, tipo_id, numero, disponible)
VALUES
    (2, 2, '201', true),
    (2, 2, '202', true),
    (2, 3, '203', true);

-- Habitaciones en el Hotel Ejemplo 3
INSERT INTO Habitaciones (hotel_id, tipo_id, numero, disponible)
VALUES
    (3, 1, '301', true),
    (3, 1, '302', true),
    (3, 2, '303', true);

INSERT INTO Clientes (nombre, apellido, correo, telefono)
VALUES
    ('Juan', 'Pérez', 'juan@example.com', '123-456-7890'),
    ('María', 'Gómez', 'maria@example.com', '987-654-3210'),
    ('Luis', 'Rodríguez', 'luis@example.com', '555-123-4567');

INSERT INTO Reservas (cliente_id, habitacion_id, fecha_entrada, fecha_salida, precio_total)
VALUES
    (1, 1, '2023-10-01', '2023-10-05', 400.00),
    (2, 5, '2023-09-15', '2023-09-18', 450.00),
    (3, 9, '2023-11-01', '2023-11-10', 850.00);


Select * from clientes;
