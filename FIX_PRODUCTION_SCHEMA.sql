-- Script SQL để thêm topic_id và learning_mode vào bảng conversations
-- Chạy script này trên Neon Console hoặc qua psql

-- Kiểm tra xem columns đã tồn tại chưa
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'conversations' 
AND column_name IN ('topic_id', 'learning_mode');

-- Thêm topic_id nếu chưa có
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'conversations' AND column_name = 'topic_id'
    ) THEN
        ALTER TABLE conversations ADD COLUMN topic_id VARCHAR(50) NULL;
        RAISE NOTICE '✅ Added topic_id column';
    ELSE
        RAISE NOTICE '⏭️  Column topic_id already exists';
    END IF;
END $$;

-- Thêm learning_mode nếu chưa có
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'conversations' AND column_name = 'learning_mode'
    ) THEN
        ALTER TABLE conversations ADD COLUMN learning_mode VARCHAR(50) NULL DEFAULT 'normal';
        RAISE NOTICE '✅ Added learning_mode column';
    ELSE
        RAISE NOTICE '⏭️  Column learning_mode already exists';
    END IF;
END $$;

-- Verify lại
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns 
WHERE table_name = 'conversations' 
ORDER BY ordinal_position;
